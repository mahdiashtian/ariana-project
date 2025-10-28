from rest_framework import serializers


class ReadArticleSerializer(serializers.Serializer):
    text = serializers.CharField()
