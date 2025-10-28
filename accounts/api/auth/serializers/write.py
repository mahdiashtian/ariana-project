from rest_framework_simplejwt import serializers as jwt_serializers

from .read import ReadTokenObtainPairSerializer


class WriteTokenObtainPairSerializer(jwt_serializers.TokenObtainPairSerializer):
    def to_representation(self, instance):
        data = ReadTokenObtainPairSerializer(instance).data
        return data
