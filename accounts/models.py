from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save

__author__ = 'Bair1'


class CustomUser(AbstractUser):
    keyboard_shortcuts = models.BooleanField(default=True)


class CallLog(models.Model):
    request = models.TextField(max_length=50)
    HttpMethod = models.TextField(max_length=7)
    user = models.ForeignKey(CustomUser)
    datetime = models.DateTimeField()


def add_user_to_dashboard_group(sender, instance, created, **kwargs):
    dashboard_group, _ = Group.objects.get_or_create(name='dashboard')
    if created:
        instance.groups.add(dashboard_group)
post_save.connect(add_user_to_dashboard_group, sender=CustomUser)
