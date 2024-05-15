from django.urls import path
from rest_framework.routers import SimpleRouter

from transactions.api.views import (
    TransactionViewSet,
    AirtimeTransaction,
    SentTransaction,
    ReceivedTransaction,
    WithdrawTransaction,
)

router = SimpleRouter()
router.register('transactions', TransactionViewSet, basename="transactions")
router.register('withdraw', WithdrawTransaction, basename="withdraw")
router.register('received', ReceivedTransaction, basename="received")
router.register('airtime', AirtimeTransaction, basename="airtime")
router.register('sent', SentTransaction, basename="sent")

urlpatterns = router.urls
