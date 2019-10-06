from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField()
    password = models.CharField(max_length=32)


class Valid_Code(models.Model):
    code_content = models.CharField(max_length=32)
    code_user = models.EmailField()
    code_time = models.DateTimeField(auto_now=True)
    code_status = models.IntegerField(default=0)  # 0 未使用 1 已使用

# Create your models here.
