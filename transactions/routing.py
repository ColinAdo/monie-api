from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('api/v1/accounts/', consumers.AccountConsumer.as_asgi()),
]