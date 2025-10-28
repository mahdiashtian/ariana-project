from rest_framework import serializers

from content.api.group.serializers import ReadGroupSerializer
from content.models import Group


class WriteGroupSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = ReadGroupSerializer(instance).data
        return data

    class Meta:
        model = Group
        fields = ['text', 'users', 'articles']
