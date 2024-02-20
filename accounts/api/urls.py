from django.urls import path

from accounts.api.views import (
    AccountApiView, 
    AccountDetailView,
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
    path('accounts/', AccountApiView.as_view(), name="accounts"),
    path('accounts/<int:pk>/', AccountDetailView.as_view(), name="account-detail"),
]