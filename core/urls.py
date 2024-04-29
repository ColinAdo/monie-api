from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('auths.urls')),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),
    path('api/v1/', include('accounts.api.urls')),
]
