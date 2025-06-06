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
    serializer_class = TransactionSerializer

    def get_queryset(self):
        # Return only transactions belonging to the logged-in user
        return Transaction.objects.filter(user=self.request.user).order_by('-created_date')



class ExpensesAnalyticsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get the year from query parameters or use the current year
        year = request.query_params.get('year', datetime.now().year)
        try:
            year = int(year)
        except ValueError:
            return Response({"error": "Invalid year parameter"}, status=400)

        # Filter transactions by year
        transactions = (
            Transaction.objects.filter(user=request.user, transaction_type='Expense', created_date__year=year)
            .annotate(month=TruncMonth('created_date'))
            .values('month')
            .annotate(total_amount=Sum('amount'))
            .order_by('month')
        )

        # Prepare data for the response
        data = []
        for i in range(1, 13):  # Iterate over all months
            month_name = datetime(1900, i, 1).strftime('%b')  # Get month name
            matching_transaction = next((t for t in transactions if t['month'].month == i), None)
            data.append({
                "name": month_name,
                "amount": matching_transaction['total_amount'] if matching_transaction else 0,
            })

        return Response({
            "year": year,
            "data": data
        })