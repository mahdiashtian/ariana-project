from .base import *


class NotFoundException(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Resource not found'
    default_code = 'not_found'


class ObjectDoesNotExist(NotFoundException):
    default_detail = 'The requested object does not exist'
    default_code = 'object_does_not_exist'


class UserNotFound(NotFoundException):
    default_detail = 'User not found'
    default_code = 'user_not_found'
