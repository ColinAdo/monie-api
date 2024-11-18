from rest_framework import viewsets, permissions

from .permissions import IsOwnerOrReadOnly

from transactions.models import Transaction
from transactions.api.serializers import (
    TransactionSerializer,
)

# Transaction viewset
class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
