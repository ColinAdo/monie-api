from rest_framework import viewsets, permissions

from .permissions import IsOwnerOrReadOnly

from transactions.models import Transaction
from transactions.api.serializers import (
    TransactionSerializer,
)

# Transaction view
class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

# Airtime transaction view
class AirtimeTransaction(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Transaction.objects.filter(transaction_type='airtime')
    serializer_class = TransactionSerializer

# Sent transaction view
class SentTransaction(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Transaction.objects.filter(transaction_type='sent')
    serializer_class = TransactionSerializer

# Received transaction view
class ReceivedTransaction(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Transaction.objects.filter(transaction_type='received')
    serializer_class = TransactionSerializer


# Withdrew transaction view
class WithdrawTransaction(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Transaction.objects.filter(transaction_type='withdraw')
    serializer_class = TransactionSerializer

