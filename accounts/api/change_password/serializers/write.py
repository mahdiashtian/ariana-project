from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from library.exceptions.validation import InvalidPassword, PasswordsDoNotMatch

User = get_user_model()


class WriteChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_repeat = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise InvalidPassword
        return value

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        new_password_repeat = attrs.get("new_password_repeat")

        if new_password != new_password_repeat:
            raise PasswordsDoNotMatch

        try:
            validate_password(new_password)
        except Exception as e:
            raise InvalidPassword(detail=str(e))

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=['password'])
        return user
