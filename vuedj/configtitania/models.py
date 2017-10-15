from django.db import models

class Config(models.Model):

    username = models.CharField(max_length=200)

    def __str__(self):
        return "Config: " + self.username
