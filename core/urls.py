from django.contrib import admin
from django.urls import path, include


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('auths.urls')),
    path('api/v1/', include('accounts.api.urls')),
    path('api/v1/', include('transactions.api.urls')),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/avi/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc',),
    path('api/v1/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
]
