from django.db import models


class UserRoleChoices(models.TextChoices):
    ADMIN = 'ADMIN'
    EDITOR = 'EDITOR'
    VIEWER = 'VIEWER'
