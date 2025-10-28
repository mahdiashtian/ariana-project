from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from content.api.article.serializers import ReadArticleSerializer, WriteArticleSerializer
from content.models import Article


@extend_schema_view(
    list=extend_schema(
        tags=["articles"],
        summary="List accessible articles",
        description="Retrieve a list of articles that the current user has access to through their groups.",
        responses={
            status.HTTP_200_OK: ReadArticleSerializer(many=True),
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
        tags=["articles"],
        summary="Retrieve an article",
        description="Get detailed information about a specific article that the user has access to.",
        responses={
            status.HTTP_200_OK: ReadArticleSerializer,
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
                description="Article not found or access denied."
            )
        }
    ),
    create=extend_schema(
        tags=["articles"],
        summary="Create a new article",
        description="Create a new article with text content.",
        request=WriteArticleSerializer,
        responses={
            status.HTTP_201_CREATED: ReadArticleSerializer,
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
                            "text": ["This field is required."]
                        }
                    ),
                    OpenApiExample(
                        name="Unique constraint",
                        value={
                            "text": ["article with this text already exists."]
                        }
                    ),
                    OpenApiExample(
                        name="Blank field",
                        value={
                            "text": ["This field may not be blank."]
                        }
                    )
                ],
                description="Validation failed."
            )
        }
    ),
    update=extend_schema(
        tags=["articles"],
        summary="Update an article",
        description="Fully update an article's text content.",
        request=WriteArticleSerializer,
        responses={
            status.HTTP_200_OK: ReadArticleSerializer,
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
                description="Article not found or access denied."
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response={"type": "object"},
                examples=[
                    OpenApiExample(
                        name="Validation error",
                        value={
                            "text": ["This field may not be blank."]
                        }
                    ),
                    OpenApiExample(
                        name="Max length exceeded",
                        value={
                            "text": ["Ensure this field has no more than 255 characters."]
                        }
                    )
                ],
                description="Validation failed."
            )
        }
    ),
    partial_update=extend_schema(
        tags=["articles"],
        summary="Partially update an article",
        description="Partially update an article's text content.",
        request=WriteArticleSerializer,
        responses={
            status.HTTP_200_OK: ReadArticleSerializer,
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
                description="Article not found or access denied."
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response={"type": "object"},
                examples=[
                    OpenApiExample(
                        name="Validation error",
                        value={
                            "text": ["This field may not be null."]
                        }
                    )
                ],
                description="Validation failed."
            )
        }
    ),
    destroy=extend_schema(
        tags=["articles"],
        summary="Delete an article",
        description="Delete a specific article.",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Article deleted successfully."
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
                description="Article not found or access denied."
            )
        }
    )
)
class ArticleViewSet(ModelViewSet):
    serializer_class = ReadArticleSerializer

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        match self.request.method.lower():
            case "get":
                serializer_class = ReadArticleSerializer
            case "put" | "post" | "patch":
                serializer_class = WriteArticleSerializer
        return serializer_class

    def get_queryset(self):
        user = self.request.user
        return Article.objects.filter(article_groups__users=user)
