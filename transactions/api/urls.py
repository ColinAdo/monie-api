from django.urls import path

from rest_framework.routers import SimpleRouter

from transactions.api.views import (
    ChatView,
    ChatWithAIPIView,
    TransactionViewSet,
    IncomeTransactionView,
    IncomeAnalyticsAPIView,
    ExpensesAnalyticsAPIView,
    ExpensesTransactionView
)

router = SimpleRouter()

router.register('transactions', TransactionViewSet, basename='transactions')

urlpatterns = [
    path('chats/', ChatView.as_view(), name='chats'),
    path('chat/ai/analytics/', ChatWithAIPIView.as_view(), name='chat-with-ai'),
    path('income/analytics/', IncomeAnalyticsAPIView.as_view(), name='incomes-analytics'),
    path('expenses/analytics/', ExpensesAnalyticsAPIView.as_view(), name='expenses-analytics'),
    path('income/transactions/', IncomeTransactionView.as_view(), name='income-transactions'),
    path('expense/transactions/', ExpensesTransactionView.as_view(), name='expenses-transactions'),
]

urlpatterns += router.urls
