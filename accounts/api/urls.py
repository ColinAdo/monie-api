from django.urls import path
from rest_framework.routers import SimpleRouter

from accounts.api.views import (
    AccountViewSet,
    TransactionViewSet,
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
]

router = SimpleRouter()
router.register('accounts', AccountViewSet, basename="accounts")
router.register('transactions', TransactionViewSet, basename="transactions")

urlpatterns += router.urls
