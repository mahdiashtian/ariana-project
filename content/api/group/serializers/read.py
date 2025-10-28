from rest_framework import serializers

from accounts.api.me.serializers import ReadMeSerializer
from content.api.article.serializers import ReadArticleSerializer


class ReadGroupSerializer(serializers.Serializer):
    users = ReadMeSerializer(many=True)
    articles = ReadArticleSerializer(many=True)
    text = serializers.CharField()
