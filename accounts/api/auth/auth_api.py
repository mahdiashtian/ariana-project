from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt import views as jwt_views

from accounts.api.auth.serializers import ReadTokenObtainPairSerializer, WriteTokenObtainPairSerializer


@extend_schema(
    tags=['Auth'],
    methods=['post'],
    filters=False,
    request=WriteTokenObtainPairSerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=ReadTokenObtainPairSerializer,
            description='Login successful',
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                    }
                )
            ]
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response={
                "type":"object",
                "properties":
                    {
                        "detail":
                         {
                             "type": "string",
                             "example": "No active account found with the given credentials"
                         }
                     },
            },
            description="Invalid credentials",
        ),
    },
    parameters=None
)
class TokenObtainPairApi(jwt_views.TokenObtainPairView):
    permission_classes = [AllowAny]
