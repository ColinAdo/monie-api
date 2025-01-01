from django.urls import path

from rest_framework.routers import SimpleRouter

from accounts.api.views import AccountViewSet, AccountPieChartAPIView

router = SimpleRouter()
router.register('accounts', AccountViewSet, basename='accounts')

urlpatterns = [
    path('account-pie-chart/', AccountPieChartAPIView.as_view(), name='account-pie-chart'),
]

urlpatterns += router.urls
