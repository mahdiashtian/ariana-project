from rest_framework.viewsets import ModelViewSet

from content.api.group.serializers import ReadGroupSerializer, WriteGroupSerializer
from content.models import Group


class GroupViewSet(ModelViewSet):
    serializer_class = ReadGroupSerializer

    def get_queryset(self):
        return Group.objects.all(
        ).prefetch_related(
            'users', 'articles'
        ).all()

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        match self.request.method.lower():
            case "get":
                serializer_class = WriteGroupSerializer
            case "put" | "post" | "patch":
                serializer_class = WriteGroupSerializer
        return serializer_class
