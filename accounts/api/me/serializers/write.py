from django.contrib.auth import get_user_model
from rest_framework import serializers

from library.exceptions.conflict import PhoneAlreadyExists, EmailAlreadyExists
from accounts.api.me.serializers.read import ReadMeSerializer

User = get_user_model()


class WriteMeSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)

    def to_representation(self, instance):
        return ReadMeSerializer(instance).data

    def validate_email(self, value):
        if User.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
            raise EmailAlreadyExists
        return value

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save(update_fields=[
            "first_name",
            "last_name",
            "email",
        ])
        return instance
