from django.urls import path

from accounts.api.views import AccountApiView

urlpatterns = [
    path('accounts/', AccountApiView.as_view(), name="accounts")
]