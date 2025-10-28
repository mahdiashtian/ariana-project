from rest_framework import serializers

from content.api.article.serializers import ReadArticleSerializer
from content.models import Article


class WriteArticleSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = ReadArticleSerializer(instance).data
        return data

    class Meta:
        model = Article
        fields = ['text']
