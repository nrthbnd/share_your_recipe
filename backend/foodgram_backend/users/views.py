from djoser.views import UserViewSet
from users.models import User
from users.serializers import CustomUserCreateSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserCreateSerializer
    # permission_classes = (,)
