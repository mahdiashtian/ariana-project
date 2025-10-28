from rest_framework import status

from library.exceptions import BaseAPIException


class ValidationException(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid data provided'
    default_code = 'validation_error'

class PasswordsDoNotMatch(ValidationException):
    default_detail = 'Passwords do not match'
    default_code = 'passwords_do_not_match'

class InvalidPassword(ValidationException):
    default_detail = 'Password does not meet the required criteria'
    default_code = 'invalid_password'
