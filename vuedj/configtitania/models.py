from django.db import models

class Config(models.Model):

    username = models.CharField(max_length=200)

    def __str__(self):
        return "Config: " + self.username

class Schema(models.Model):
    version = models.CharField(max_length=4)
    major_version = models.CharField(max_length=2)
    minor_version = models.CharField(max_length=3)
