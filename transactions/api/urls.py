from django.urls import path

from rest_framework.routers import SimpleRouter

from transactions.api.views import (
    ChatWithAIAPIView,
    TransactionViewSet,
    IncomeAnalyticsAPIView,
    ExpensesAnalyticsAPIView,
)

router = SimpleRouter()

router.register('transactions', TransactionViewSet, basename='transactions')

urlpatterns = [
    path('chat/ai/analytics/', ChatWithAIAPIView.as_view(), name='chat-with-ai'),
    path('income/analytics/', IncomeAnalyticsAPIView.as_view(), name='incomes-analytics'),
    path('expenses/analytics/', ExpensesAnalyticsAPIView.as_view(), name='expenses-analytics'),
]

urlpatterns += router.urls
