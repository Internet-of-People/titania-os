from .models import SessionDetails
from rest_framework import serializers

class SessionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionDetails
        fields = '__all__'