from rest_framework import generics

from accounts.models import Account, Transaction
from accounts.api.serializers import (
    AccountSerializer,
    TransactionSerializer,
)

class AccountApiView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionApilistView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TrnsactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class AirtimeTransaction(generics.ListAPIView):
    queryset = Transaction.objects.filter(transaction_type='airtime')
    serializer_class = TransactionSerializer


class SentTransaction(generics.ListAPIView):
    queryset = Transaction.objects.filter(transaction_type='sent')
    serializer_class = TransactionSerializer


class ReceivedTransaction(generics.ListAPIView):
    queryset = Transaction.objects.filter(transaction_type='received')
    serializer_class = TransactionSerializer


class WithdrawTransaction(generics.ListAPIView):
    queryset = Transaction.objects.filter(transaction_type='withdraw')
    serializer_class = TransactionSerializer

