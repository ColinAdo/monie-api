from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from accounts.api.serializers import AccountSerializer

from .permissions import IsOwnerOrReadOnly

# Account viewset
class AccountViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Account.objects.all().order_by('-created_date')
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AccountPieChartAPIView(APIView):
    def get(self, request):
        accounts = Account.objects.all()
        data = [{"name": account.name, "value": float(account.amount)} for account in accounts]
        return Response(data)
