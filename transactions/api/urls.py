from django.urls import path

from rest_framework.routers import SimpleRouter

from transactions.api.views import (
    TransactionViewSet,
    TransactionAnalyticsAPIView
)

router = SimpleRouter()

router.register('transactions', TransactionViewSet, basename='transactions')

urlpatterns = [
    path('transaction/analytics/', TransactionAnalyticsAPIView.as_view(), name='transaction-analytics'),
]

urlpatterns += router.urls
