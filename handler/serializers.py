from rest_framework import serializers

from .models import Deal


class DealSerializer(serializers.ModelSerializer):
    """Serializer for your model, handling field validation."""

    class Meta:
        model = Deal
        fields = ['full_name', 'phone_number', 'comment']

    def validate_phone_number(self, value):
        """Raises an error if the value is not a digit"""

        if not value.isdigit():
            raise serializers.ValidationError("Phone number must consist of digits only.")
        return value
    
    def validate_full_name(self, value):
        """Raises an error if the value is not a str"""
        
        if value.isdigit():
            raise serializers.ValidationError("Phone number must be a string.")
        return value