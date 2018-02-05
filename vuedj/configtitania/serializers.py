from .models import BoxDetails
from rest_framework import serializers

class BoxDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxDetails
        fields = '__all__'