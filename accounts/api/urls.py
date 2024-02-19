from django.urls import path

from accounts.api.views import (
    AccountApiView, 
    AccountDetailView,
    TransactionApilistView,
    TrnsactionDetailView,
)

urlpatterns = [
    path('transactions/', TransactionApilistView.as_view(), name="transactions"),
    path('transactions/<int:pk>/', TrnsactionDetailView.as_view(), name="transaction-detail"),
    path('accounts/', AccountApiView.as_view(), name="accounts"),
    path('accounts/<int:pk>/', AccountDetailView.as_view(), name="account-detail"),
]