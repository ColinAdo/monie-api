from rest_framework import serializers

from accounts.models import Account
from transactions.api.serializers import TransactionSerializer

# Account serializer
class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)
    transactions_count = serializers.SerializerMethodField()

    def get_transactions_count(self, obj):
        return obj.transactions.count()

    class Meta:
        model = Account
        fields = (
            'id',
            'balance',
            'created_date',
            'transactions',
            'transactions_count'
        )
