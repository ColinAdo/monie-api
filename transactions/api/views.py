from rest_framework import viewsets, permissions

from .permissions import IsOwnerOrReadOnly

from transactions.models import Transaction
from transactions.api.serializers import (
    TransactionSerializer,
)

# Transaction viewset
class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Transaction.objects.all().order_by('-created_date')
    serializer_class = TransactionSerializer
