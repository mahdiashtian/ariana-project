from rest_framework import status

from library.exceptions import BaseAPIException


class ConflictException(BaseAPIException):
    """Base class for conflict exceptions"""
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Resource conflict'
    default_code = 'conflict'

class EmailAlreadyExists(ConflictException):
    default_detail = 'This email is already registered'
    default_code = 'email_already_exists'


class UsernameAlreadyExists(ConflictException):
    default_detail = 'This username is already taken'
    default_code = 'username_already_exists'


class PhoneAlreadyExists(ConflictException):
    default_detail = 'This phone number is already registered'
    default_code = 'phone_already_exists'
