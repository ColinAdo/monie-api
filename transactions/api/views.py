from rest_framework import viewsets, permissions

from transactions.models import Transaction
from .permissions import IsOwnerOrReadOnly
from transactions.api.serializers import (
    TransactionSerializer,
)

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class AirtimeTransaction(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Transaction.objects.filter(transaction_type='airtime')
    serializer_class = TransactionSerializer


class SentTransaction(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Transaction.objects.filter(transaction_type='sent')
    serializer_class = TransactionSerializer


class ReceivedTransaction(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Transaction.objects.filter(transaction_type='received')
    serializer_class = TransactionSerializer


# Withdrew transaction view
class WithdrawTransaction(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Transaction.objects.filter(transaction_type='withdraw')
    serializer_class = TransactionSerializer

