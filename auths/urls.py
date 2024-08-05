from django.urls import path, re_path

from .views import (
    CustomProviderAuthView,
    LogoutView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView
)


urlpatterns = [
    re_path(
        r'^o/(?P<provider>\S+)/$',
        CustomProviderAuthView.as_view(),
        name='provider-auth'
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
]
