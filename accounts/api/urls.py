from rest_framework.routers import SimpleRouter

from accounts.api.views import AccountViewSet

router = SimpleRouter()
router.register('accounts', AccountViewSet, basename='accounts')

urlpatterns = router.urls
