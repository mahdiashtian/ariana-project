from rest_framework import serializers

from accounts.models import Knowledge


class WriteKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Knowledge
        fields = [
            "text",
            "summary"
        ]
