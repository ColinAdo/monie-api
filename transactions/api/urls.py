from django.urls import path

from rest_framework.routers import SimpleRouter

from transactions.api.views import (
    TransactionViewSet,
    ExpensesAnalyticsAPIView
)

router = SimpleRouter()

router.register('transactions', TransactionViewSet, basename='transactions')

urlpatterns = [
    path('expenses/analytics/', ExpensesAnalyticsAPIView.as_view(), name='expenses-analytics'),
]

urlpatterns += router.urls
