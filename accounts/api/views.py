from rest_framework import generics

from accounts.models import Account
from accounts.api.serializers import AccountSerializer

class AccountApiView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer