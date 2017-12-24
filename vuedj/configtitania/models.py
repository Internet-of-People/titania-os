from django.db import models

class BoxDetails(models.Model):
    boxname = models.CharField(max_length=64)

class RegisteredServices(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=254)
    icon = models.CharField(max_length=2048)
