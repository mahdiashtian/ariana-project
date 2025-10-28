from rest_framework.exceptions import APIException
from rest_framework import status


class BaseAPIException(APIException):

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Internal server error."
    default_code = 'server_error'

    def __init__(self, detail=None, code=None, status_code=None):
        if detail is not None:
            self.detail = detail
        if code is not None:
            self.default_code = code
        if status_code is not None:
            self.status_code = status_code
        super().__init__(detail, code)