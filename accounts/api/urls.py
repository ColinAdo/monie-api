from django.urls import path
from rest_framework.routers import SimpleRouter

from accounts.api.views import (
    AccountViewSet,
    TransactionApilistView,
    TrnsactionDetailView,
    AirtimeTransaction,
    SentTransaction,
    ReceivedTransaction,
    WithdrawTransaction,
)

urlpatterns = [
    path('transactions/withdraw/', WithdrawTransaction.as_view(), name="withdraw"),
    path('transactions/received/', ReceivedTransaction.as_view(), name="received"),
    path('transactions/sent/', SentTransaction.as_view(), name="sent"),
    path('transactions/airtime/', AirtimeTransaction.as_view(), name="airtime"),

    path('transactions/', TransactionApilistView.as_view(), name="transactions"),
    path('transactions/<int:pk>/', TrnsactionDetailView.as_view(), name="transaction-detail"),
]

router = SimpleRouter()
router.register('', AccountViewSet, basename="accounts")

urlpatterns += router.urls
