from djoser.views import UserViewSet
from .serializers import CustomUserCreateSerializer

class CustomUserCreateView(UserViewSet):
    serializer_class = CustomUserCreateSerializer

