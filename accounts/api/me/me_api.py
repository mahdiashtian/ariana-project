from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from accounts.api.me.serializers import ReadMeSerializer, WriteMeSerializer
from library.exceptions import UserNotFound

User = get_user_model()


@extend_schema_view(
    get=extend_schema(
        tags=["me"],
        summary="Get current user profile",
        description="Retrieve the profile information of the currently authenticated user.",
        responses={
            status.HTTP_200_OK: ReadMeSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Authentication credentials were not provided."
                        }
                    }
                },
                description="Authentication required."
            )
        }
    ),
    patch=extend_schema(
        tags=["me"],
        summary="Update current user profile",
        description="Partially update the profile information of the currently authenticated user.",
        request=WriteMeSerializer,
        responses={
            status.HTTP_200_OK: ReadMeSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Authentication credentials were not provided."
                        }
                    }
                },
                description="Authentication required."
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response={"type": "object"},
                examples=[
                    OpenApiExample(
                        name="Phone number conflict",
                        value={
                            "detail": "Phone number already exists"
                        }
                    ),
                    OpenApiExample(
                        name="Email conflict",
                        value={
                            "detail": "Email already exists"
                        }
                    ),
                    OpenApiExample(
                        name="Validation error",
                        value={
                            "first_name": ["This field is required."],
                            "email": ["Enter a valid email address."]
                        }
                    )
                ],
                description="Validation failed."
            )
        }
    ),
    put=extend_schema(
        tags=["me"],
        summary="Update current user profile",
        description="Fully update the profile information of the currently authenticated user.",
        request=WriteMeSerializer,
        responses={
            status.HTTP_200_OK: ReadMeSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Authentication credentials were not provided."
                        }
                    }
                },
                description="Authentication required."
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response={"type": "object"},
                examples=[
                    OpenApiExample(
                        name="Phone number conflict",
                        value={
                            "detail": "Phone number already exists"
                        }
                    ),
                    OpenApiExample(
                        name="Email conflict",
                        value={
                            "detail": "Email already exists"
                        }
                    ),
                    OpenApiExample(
                        name="Validation error",
                        value={
                            "first_name": ["This field is required."],
                            "email": ["Enter a valid email address."]
                        }
                    )
                ],
                description="Validation failed."
            )
        }
    )
)
class MeApi(UpdateAPIView, RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch", "put"]
    lookup_field = "id"

    def get_object(self):
        user: User = self.queryset.filter(id=self.request.user.id).first()
        if user is None:
            raise UserNotFound
        return user

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        match self.request.method.lower():
            case "get":
                serializer_class = ReadMeSerializer
            case "patch" | "put":
                serializer_class = WriteMeSerializer
        return serializer_class
