from .models import Config
from rest_framework import serializers

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ('username',)
