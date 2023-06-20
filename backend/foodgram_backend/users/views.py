from djoser.views import UserViewSet

from users.serializers import CustomUserCreateSerializer
from users.models import User


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserCreateSerializer
