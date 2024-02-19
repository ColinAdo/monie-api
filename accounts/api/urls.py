from django.urls import path

from accounts.api.views import (
    AccountApiView, 
    AccountDetailView,
    TransactionApilistView,
)

urlpatterns = [
    path('transactions/', TransactionApilistView.as_view(), name="transactions"),
    path('accounts/', AccountApiView.as_view(), name="accounts"),
    path('accounts/<int:pk>/', AccountDetailView.as_view(), name="account-detail"),
]