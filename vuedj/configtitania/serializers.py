from .models import Config, Schema
from rest_framework import serializers

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ('username',)

class SchemaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Schema
        fields = ('version', 'major_version', 'minor_version')
