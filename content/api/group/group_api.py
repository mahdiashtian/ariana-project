from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from content.api.group.serializers import ReadGroupSerializer, WriteGroupSerializer
from content.models import Group


@extend_schema_view(
    list=extend_schema(
        tags=["groups"],
        summary="List all groups",
        description="Retrieve a list of all groups with their users and articles.",
        responses={
            status.HTTP_200_OK: ReadGroupSerializer(many=True),
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
    retrieve=extend_schema(
        tags=["groups"],
        summary="Retrieve a group",
        description="Get detailed information about a specific group including its users and articles.",
        responses={
            status.HTTP_200_OK: ReadGroupSerializer,
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
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Not found."
                        }
                    }
                },
                description="Group not found."
            )
        }
    ),
    create=extend_schema(
        tags=["groups"],
        summary="Create a new group",
        description="Create a new group with text, users and articles.",
        request=WriteGroupSerializer,
        responses={
            status.HTTP_201_CREATED: ReadGroupSerializer,
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
                        name="Validation error",
                        value={
                            "text": ["This field is required."],
                            "users": ["This list may not be empty."],
                            "articles": ["Invalid pk \"100\" - object does not exist."]
                        }
                    ),
                    OpenApiExample(
                        name="Unique constraint",
                        value={
                            "text": ["group with this text already exists."]
                        }
                    )
                ],
                description="Validation failed."
            )
        }
    ),
    update=extend_schema(
        tags=["groups"],
        summary="Update a group",
        description="Fully update a group including its users and articles.",
        request=WriteGroupSerializer,
        responses={
            status.HTTP_200_OK: ReadGroupSerializer,
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
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Not found."
                        }
                    }
                },
                description="Group not found."
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response={"type": "object"},
                examples=[
                    OpenApiExample(
                        name="Validation error",
                        value={
                            "text": ["This field may not be blank."],
                            "users": ["Expected a list of items but got type \"string\"."]
                        }
                    )
                ],
                description="Validation failed."
            )
        }
    ),
    partial_update=extend_schema(
        tags=["groups"],
        summary="Partially update a group",
        description="Partially update a group's information, users, or articles.",
        request=WriteGroupSerializer,
        responses={
            status.HTTP_200_OK: ReadGroupSerializer,
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
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Not found."
                        }
                    }
                },
                description="Group not found."
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response={"type": "object"},
                examples=[
                    OpenApiExample(
                        name="Validation error",
                        value={
                            "text": ["This field may not be null."],
                            "users": ["Invalid pk \"abc\" - expected a number."]
                        }
                    )
                ],
                description="Validation failed."
            )
        }
    ),
    destroy=extend_schema(
        tags=["groups"],
        summary="Delete a group",
        description="Delete a specific group.",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Group deleted successfully."
            ),
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
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response={
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Not found."
                        }
                    }
                },
                description="Group not found."
            )
        }
    )
)
class GroupViewSet(ModelViewSet):
    serializer_class = ReadGroupSerializer

    def get_queryset(self):
        return Group.objects.all().prefetch_related('users', 'articles')

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        match self.request.method.lower():
            case "get":
                serializer_class = ReadGroupSerializer
            case "put" | "post" | "patch":
                serializer_class = WriteGroupSerializer
        return serializer_class
