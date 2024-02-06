import os
from rest_framework import serializers
from dotenv import load_dotenv

load_dotenv()

class HandlerSerializer(serializers.Serializer):
    """Serializer for handling API calls from bitrix24"""

    auth_token = serializers.CharField()
    order_id = serializers.IntegerField()

    def validate_auth_token_token(self, value):
        """Checks if the request was sent by bitrix24"""
        
        if value != os.getenv("BITRIX_AUTHENTICATION"):
            raise serializers.ValidationError("Authentication code doesn't match")
        
        return value
    

class ContactIDSerializer(serializers.Serializer):
    """Serializer for handling contact id from bitrix24"""

    CONTACT_ID = serializers.IntegerField()


class OrderContactSerializer(serializers.Serializer):
    """serializer for handling the order results from bitrix24"""

    result = serializers.ListField(child=ContactIDSerializer())


class PhoneSerializer(serializers.Serializer):
    """Serializer for handling the value of the phone number from bitrix24"""

    VALUE = serializers.CharField(max_length=30)


class ContactInfoSerializer(serializers.Serializer):
    """Serializer for handling contact information from bitrix24"""

    NAME = serializers.CharField(max_length=99)
    SECOND_NAME = serializers.CharField(max_length=99, allow_null=True, allow_blank=True)
    LAST_NAME = serializers.CharField(max_length=99)
    COMMENTS = serializers.CharField(max_length=599, allow_null=True)
    HAS_PHONE  = serializers.BooleanField()
    PHONE = serializers.ListField(child=PhoneSerializer())

    def validate_has_phone(self, value):
        if value != True:
            raise serializers.ValidationError("The contact doesn't have a phone number")
        

class ContactSerializer(serializers.Serializer):
    """Serializer for handling contact information results from bitrix24"""

    result = ContactInfoSerializer()
