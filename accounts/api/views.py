from rest_framework import viewsets, permissions

from accounts.models import Account
from accounts.api.serializers import AccountSerializer

from .permissions import IsOwnerOrReadOnly

# Account viewset
class AccountViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


