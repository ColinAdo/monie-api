from rest_framework import serializers

from accounts.models import Account, Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = (
            'id',
            'balance',
            'created_date',
        )
