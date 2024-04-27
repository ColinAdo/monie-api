from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from django.conf import settings
import boto3


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):  # Inherit from UserCreateSerializer.Meta
        model = get_user_model()
        fields = ('username', 'phone_number')


    def create(self, validated_data):
        user = get_user_model().objects.create(**validated_data)

        # Send your sms message.
        client = boto3.client(
            "sns",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME
        )

        response = client.publish(
            PhoneNumber=settings.SMS_MOBILE,
            Message=settings.SMS_MESSAGE,
            MessageAttributes={
                'AWS.SNS.SMS.SenderID': {
                    'DataType': 'String',
                    'StringValue': settings.SENDER_ID
                }
            }
        )

        # Generating a random PIN might be better for security
        # user.pin = generate_random_pin()

        # Instead, let's just save the message sent for reference
        user.pin = settings.SMS_MESSAGE
        user.save()

        return user
