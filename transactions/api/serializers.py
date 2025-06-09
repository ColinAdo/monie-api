from rest_framework import serializers

from transactions.models import Transaction, Chat

# Transaction serializer
class TransactionSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source='account.name', read_only=True)
    class Meta:
        model = Transaction
        fields = [
            'id', 
            'account_name', 
            'description', 
            'amount', 
            'transaction_type', 
            'created_date'
        ]

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'