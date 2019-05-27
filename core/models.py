from django.contrib.auth.models import User
from django.db import models


class Joke(models.Model):
    text = models.TextField(db_index=True)
    users = models.ManyToManyField(to=User, related_name='jokes')


class ActionHistory(models.Model):
    user = models.ForeignKey(to=User, related_name='actions', null=True, on_delete=models.SET_NULL)
    ip = models.GenericIPAddressField()
    created_at = models.DateTimeField()
