# accounts/middleware/jwt_auth.py
import logging
from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from jwt import decode as jwt_decode, DecodeError, ExpiredSignatureError

logger = logging.getLogger(__name__)
User = get_user_model()


class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware for JWT authentication in Django Channels.
    Supports token in:
    - Authorization header: Bearer <token>
    - Query string: ?token=<token>
    """

    async def __call__(self, scope, receive, send):
        # Extract token from headers or query string
        token = self._get_token_from_scope(scope)

        if token:
            scope["user"] = await self._get_user_from_token(token)
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    def _get_token_from_scope(self, scope):
        """
        Extract JWT token from headers or query string.

        Priority:
        1. Authorization header (Bearer token)
        2. Query string (?token=xxx)
        """
        # Try to get token from Authorization header
        headers = dict(scope.get('headers', []))

        if bytes('authorization','utf-8') in headers:
            try:

                auth_header = headers[b'authorization'].decode()
                token_type, token = auth_header.split(maxsplit=1)
                if token_type.lower() == 'jwt':
                    return token.strip()
            except (ValueError, UnicodeDecodeError) as e:
                logger.warning(f"Invalid authorization header format: {e}")

        # Fallback: Try to get token from query string
        query_string = scope.get('query_string', b'').decode()
        if query_string:
            query_params = parse_qs(query_string)
            token = query_params.get('token', [None])[0]
            if token:
                return token

        return None

    async def _get_user_from_token(self, token):
        """
        Validate JWT token and return associated user.

        Args:
            token (str): JWT token

        Returns:
            User or AnonymousUser
        """
        try:
            # Decode and validate token
            payload = jwt_decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )

            # Get user from database
            user = await self._get_user_by_id(payload.get("user_id"))

            if user and user.is_active:
                return user
            else:
                logger.warning(f"User not found or inactive for token: {payload.get('user_id')}")
                return AnonymousUser()

        except ExpiredSignatureError:
            logger.warning("JWT token has expired")
            return AnonymousUser()

        except DecodeError as e:
            logger.warning(f"JWT decode error: {e}")
            return AnonymousUser()

        except Exception as e:
            logger.error(f"Unexpected error in JWT authentication: {e}")
            return AnonymousUser()

    @database_sync_to_async
    def _get_user_by_id(self, user_id):
        """
        Retrieve user from database by ID.

        Args:
            user_id: User primary key

        Returns:
            User instance or None
        """
        if not user_id:
            return None

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def jwt_auth_middleware_stack(inner):
    """
    Convenience function to apply JWT auth middleware with Django's auth middleware.

    Usage in routing.py:
        from accounts.middleware.jwt_auth import JWTAuthMiddlewareStack

        application = ProtocolTypeRouter({
            "websocket": JWTAuthMiddlewareStack(
                URLRouter(
                    websocket_urlpatterns
                )
            ),
        })
    """
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))
