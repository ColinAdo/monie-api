from rest_framework import serializers

from transactions.models import Transaction

# Transaction serializer
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


