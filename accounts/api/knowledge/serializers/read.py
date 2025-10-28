from rest_framework import serializers


class ReadKnowledgeSerializer(serializers.Serializer):
    text = serializers.CharField()
    summary = serializers.CharField(required=False)
