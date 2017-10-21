from django.db import models

class User(models.Model):

    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    boxname = models.CharField(max_length=64)

class Schema(models.Model):
    version = models.CharField(max_length=3)
    major_version = models.CharField(max_length=1)
    minor_version = models.CharField(max_length=2)
