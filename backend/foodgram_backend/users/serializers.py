from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.fields import SerializerMethodField
from users.models import Follow, User


class CustomUserCreateSerializer(UserCreateSerializer):
    """Создание пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'first_name',
                  'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    """Получает поля пользователя (SAFE_METHODS)."""
    is_subscribed = SerializerMethodField(method_name='get_subscription')

    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'first_name',
                  'last_name', 'is_subscribed',)
        read_only_fields = ('is_subscribed',)

    def get_subscription(self, obj):
        """Возвращает True/False о подписке на автора рецепта
        пользователя, отправляющего запрос."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()
