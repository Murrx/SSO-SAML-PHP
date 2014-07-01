from django.contrib.auth.models import AbstractUser
from django.db import models

__author__ = 'Bair1'


class CustomUser(AbstractUser):
    keyboard_shortcuts = models.BooleanField(default=True)

