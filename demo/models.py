from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    id = models.BigAutoField(primary_key=True)
    nickname = models.CharField(max_length=64, null=True)
    gender = models.IntegerField(default=0, null=True)
    phone = models.CharField(max_length=32, null=True)
    is_ban = models.IntegerField(default=0)
    role = models.CharField(max_length=20)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username

