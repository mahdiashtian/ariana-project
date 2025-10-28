from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from accounts.api.knowledge.serializers import ReadKnowledgeSerializer, WriteKnowledgeSerializer
from accounts.models import Knowledge


@extend_schema_view(
    list=extend_schema(
        tags=["knowledge"],
        summary="List all knowledge items",
        description="Retrieve a list of all knowledge items with search capability.",
        responses={
            status.HTTP_200_OK: ReadKnowledgeSerializer(many=True),
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
        },
        parameters=[
            {
                "name": "search",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "string"
                },
                "description": "Search in knowledge text"
            }
        ]
    ),
    retrieve=extend_schema(
        tags=["knowledge"],
        summary="Retrieve a knowledge item",
        description="Get detailed information about a specific knowledge item.",
        responses={
            status.HTTP_200_OK: ReadKnowledgeSerializer,
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
                description="Knowledge item not found."
            )
        }
    ),
    create=extend_schema(
        tags=["knowledge"],
        summary="Create a new knowledge item",
        description="Create a new knowledge item with text and summary.",
        request=WriteKnowledgeSerializer,
        responses={
            status.HTTP_201_CREATED: ReadKnowledgeSerializer,
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
                            "summary": ["This field may not be blank."]
                        }
                    )
                ],
                description="Validation failed."
            )
        }
    ),
    update=extend_schema(
        tags=["knowledge"],
        summary="Update a knowledge item",
        description="Fully update a knowledge item.",
        request=WriteKnowledgeSerializer,
        responses={
            status.HTTP_200_OK: ReadKnowledgeSerializer,
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
                description="Knowledge item not found."
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response={"type": "object"},
                examples=[
                    OpenApiExample(
                        name="Validation error",
                        value={
                            "text": ["This field is required."],
                            "summary": ["This field may not be blank."]
                        }
                    )
                ],
                description="Validation failed."
            )
        }
    ),
    partial_update=extend_schema(
        tags=["knowledge"],
        summary="Partially update a knowledge item",
        description="Partially update a knowledge item.",
        request=WriteKnowledgeSerializer,
        responses={
            status.HTTP_200_OK: ReadKnowledgeSerializer,
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
                description="Knowledge item not found."
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response={"type": "object"},
                examples=[
                    OpenApiExample(
                        name="Validation error",
                        value={
                            "text": ["This field may not be null."],
                            "summary": ["This field is too long."]
                        }
                    )
                ],
                description="Validation failed."
            )
        }
    ),
    destroy=extend_schema(
        tags=["knowledge"],
        summary="Delete a knowledge item",
        description="Delete a specific knowledge item.",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Knowledge item deleted successfully."
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
                description="Knowledge item not found."
            )
        }
    )
)
class KnowledgeViewSet(ModelViewSet):
    queryset = Knowledge.objects.all()
    serializer_class = ReadKnowledgeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['text']

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        match self.request.method.lower():
            case "get":
                serializer_class = ReadKnowledgeSerializer
            case "put" | "post" | "patch":
                serializer_class = WriteKnowledgeSerializer
        return serializer_class