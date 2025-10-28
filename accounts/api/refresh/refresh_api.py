from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt import serializers as jwt_serializers

@extend_schema(
    tags=['Auth'],
    methods=['POST'],
    filters=False,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=jwt_serializers.TokenRefreshSerializer,
            description="Token refreshed successfully",
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                    }
                )
            ]
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string",
                        "example": "Token is invalid or expired"
                    },
                    "code": {
                        "type": "string",
                        "example": "token_not_valid"
                    }
                }
            },
            description="Invalid or expired refresh token",
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "refresh": {
                        "type": "string",
                        "example": "This field is required."
                    }
                }
            },
            description="Refresh token missing",
        )
    },
    parameters=None
)
class TokenRefreshApi(jwt_views.TokenRefreshView):
    permission_classes = [AllowAny]