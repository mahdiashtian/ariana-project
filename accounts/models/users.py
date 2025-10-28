from django.contrib.auth.models import AbstractUser
from django.db import models

from library.choices import UserRoleChoices


class User(AbstractUser):
    role = models.CharField(choices=
                            UserRoleChoices.choices, default=UserRoleChoices.VIEWER.value)

    is_staff = None
