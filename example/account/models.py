from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_extensions.fields import DictField, ColorField


class User(AbstractUser):
    extra = ColorField(null=True)
    pass
