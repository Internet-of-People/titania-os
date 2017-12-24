from .models import BoxDetails, RegisteredServices
from rest_framework import serializers

class BoxDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxDetails
        fields = '__all__'

class RegisteredServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredServices
        fields = '__all__'