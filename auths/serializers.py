
import boto3
import random
from django.conf import settings
from djoser.serializers import UserCreateSerializer
from .models import CustomUser
from django.contrib.auth.hashers import make_password


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('username', 'phone_number')

    def create(self, validated_data):
        validated_data['password'] = None
        pin = settings.SMS_MESSAGE
        validated_data['pin'] = make_password(str(pin))  # Hash the pin
        return super().create(validated_data)
    
    def validate(self, attrs):
        if 'password' in attrs:
            del attrs['password']
        return attrs
    
    # Deluxe pin: 16417

    # Send your sms message.
    # client = boto3.client(
    #     "sns",
    #     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    #     region_name=settings.AWS_REGION_NAME
    # )

    # response = client.publish(
    #     PhoneNumber=settings.SMS_MOBILE,
    #     Message=settings.SMS_MESSAGE,
    #     MessageAttributes={
    #         'AWS.SNS.SMS.SenderID': {
    #             'DataType': 'String',
    #             'StringValue': settings.SENDER_ID
    #         }
    #     }
    # )
    print(settings.SMS_MESSAGE)

    


