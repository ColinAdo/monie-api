from django.urls import path

from rest_framework.routers import SimpleRouter

from transactions.api.views import TransactionViewSet

router = SimpleRouter()

router.register('transactions', TransactionViewSet, basename='transactions')

urlpatterns = router.urls
