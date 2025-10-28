from rest_framework.viewsets import ModelViewSet

from content.api.article.serializers import ReadArticleSerializer, WriteArticleSerializer
from content.models import Article


class ArticleViewSet(ModelViewSet):
    serializer_class = ReadArticleSerializer

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        match self.request.method.lower():
            case "get":
                serializer_class = WriteArticleSerializer
            case "put" | "post" | "patch":
                serializer_class = WriteArticleSerializer
        return serializer_class

    def get_queryset(self):
        user = self.request.user
        return Article.objects.filter(article_groups__users=user)
