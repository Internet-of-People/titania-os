from django.db import models

class SessionDetails(models.Model):
    session_key = models.CharField(max_length=30)
    username = models.CharField(max_length=255)
    client_ip = models.CharField(max_length=255)

