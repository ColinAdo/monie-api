from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('auths.urls')),
    path('api/v1/', include('accounts.api.urls')),
    path('api/v1/', include('transactions.api.urls')),
]
