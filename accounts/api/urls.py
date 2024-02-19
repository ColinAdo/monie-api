from django.urls import path

from accounts.api.views import (
    AccountApiView, 
    AccountDetailView,
    TransactionApilistView,
    TrnsactionDetailView,
    NotificationApilistView,
    NotificationDetailView,
)

urlpatterns = [
    path('notifications/', NotificationApilistView.as_view(), name="notifications"),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name="notification-detail"),
    path('transactions/', TransactionApilistView.as_view(), name="transactions"),
    path('transactions/<int:pk>/', TrnsactionDetailView.as_view(), name="transaction-detail"),
    path('accounts/', AccountApiView.as_view(), name="accounts"),
    path('accounts/<int:pk>/', AccountDetailView.as_view(), name="account-detail"),
]