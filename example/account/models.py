from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_extensions.fields import DictField, ColorField, Color


class User(AbstractUser):
    fav_color = ColorField(default=Color.default)
    pass
