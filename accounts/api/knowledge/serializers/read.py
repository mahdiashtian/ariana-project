from rest_framework import serializers


class ReadKnowledgeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    summary = serializers.CharField(required=False)
