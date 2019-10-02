from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField()
    password = models.CharField(max_length=32)


# Create your models here.
