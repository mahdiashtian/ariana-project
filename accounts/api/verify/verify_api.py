from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt import views as jwt_views


@extend_schema(
    tags=['Auth'],
    methods=['POST'],
    filters=False,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response={},
            description="Token is valid"
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
            description="Token is invalid or expired"
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "token": {
                        "type": "list",
                        "example": ["This field may not be blank."]
                    }
                }
            },
            description="Token missing"
        )
    },
    parameters=None
)
class TokenVerifyApi(jwt_views.TokenVerifyView):
    permission_classes = [AllowAny]