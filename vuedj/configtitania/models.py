from django.db import models

class BoxDetails(models.Model):
    boxname = models.CharField(max_length=64)
