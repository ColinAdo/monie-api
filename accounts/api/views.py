from rest_framework import generics, viewsets, permissions

from accounts.models import Account, Transaction
from .permissions import IsOwnerOrReadOnly
from accounts.api.serializers import (
    AccountSerializer,
    TransactionSerializer,
)

class AccountViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
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

