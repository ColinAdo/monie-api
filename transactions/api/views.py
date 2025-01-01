from django.db.models.functions import TruncMonth
from django.db.models import Sum

from datetime import datetime

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

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


class TransactionAnalyticsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request):
        transactions = (
            Transaction.objects.annotate(month=TruncMonth('created_date'))
            .values('month')
            .annotate(total_amount=Sum('amount'))
            .order_by('month')
        )

        data = []
        for i in range(1, 13):  # Iterate over all months (January to December)
            month_name = datetime(1900, i, 1).strftime('%b')  # Get month name
            matching_transaction = next((t for t in transactions if t['month'].month == i), None)
            data.append({
                "name": month_name,
                "amount": matching_transaction['total_amount'] if matching_transaction else 0,
            })

        return Response(data)
