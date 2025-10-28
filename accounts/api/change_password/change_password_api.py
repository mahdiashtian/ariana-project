from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.change_password.serializers import WriteChangePasswordSerializer


@extend_schema(
    tags=["change-password"],
    methods=["post"],
    filters=None,
    parameters=None,
    request=WriteChangePasswordSerializer,
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "str",
                        "example": "Password changed successfully."
                    }
                }
            },
            description="Password changed."
        ), status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response={
                "type": "object",
                "properties":
                    {
                        "detail":
                            {
                                "type": "string",
                                "example": "No active account found with the given credentials"
                            }
                    },
            },
            description="Invalid credentials.",
        ), status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response={
                "type": "object"
            },
            examples=[
                OpenApiExample(
                    name="Password does not match",
                    value={
                        "detail": "Password does not meet the required criteria"
                    }
                ), OpenApiExample(
                    name="Field error",
                    value=
                    {
                        "detail": "['This password is too short. It must contain at least 8 characters.', 'This password is too common.', 'This password is entirely numeric.']"
                    }
                ),
            ],description="Password invalid."
        )
    }

)
class ChangePasswordApi(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WriteChangePasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
