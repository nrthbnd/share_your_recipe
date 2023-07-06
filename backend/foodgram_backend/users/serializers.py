from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from recipes.models import Recipes
from users.models import Follow, User


class CustomUserCreateSerializer(UserCreateSerializer):
    """Создание пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'first_name',
                  'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    """Сериалайзер для получени информации о пользователях."""
    is_subscribed = SerializerMethodField(
        method_name='get_subscription')

    class Meta:
        model = User
        fields = ("email", "id", "username",
                  "first_name", "last_name",
                  "is_subscribed")

    def get_subscription(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Follow.objects.filter(user=user, author=obj).exists()
        return False


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки на автора рецепта."""
    is_subscribed = SerializerMethodField(
        method_name='get_subscription)
    recipes = SerializerMethodField(
        method_name='get_recipes')
    recipes_count = SerializerMethodField(
        method_name='get_recipes_count')

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def validate(self, data):
        author = self.instance
        user = self.context['request'].user
        method = self.context['request'].method
        if method == 'POST':
            if user == author:
                raise serializers.ValidationError(
                    'На себя подписаться нельзя.')

            if Follow.objects.filter(user=user, author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже подписаны на данного автора.')

        if method == 'DELETE':
            if not Follow.objects.filter(user=user, author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже отписались от данного автора или '
                    'не были подписаны на него.')
        return data

    def get_major_serialiser(self):
        """Решение проблемы перекрестного импорта с сериализатором из апи."""
        from api.serializers import RecipesMajorSerializer
        return RecipesMajorSerializer

    def get_subscription(self, obj):
        """Возвращает True/False о подписке на автора рецепта
        пользователя, отправляющего запрос."""
        user = self.context["request"].user
        if user.is_authenticated:
            return Follow.objects.filter(user=user, author=obj).exists()
        return False

    def get_recipes(self, obj):
        """Получает рецепты автора, на которого оформлена подписка
        (c учетом лимита)."""
        request = self.context.get('request')
        recipes = Recipes.objects.filter(author=obj)
        recipes_limit = request.GET.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        serializer = self.get_major_serialiser()(
            recipes,
            context={'request': request},
            many=True,
            read_only=True)
        return serializer.data

    def get_recipes_count(self, obj):
        """Получает количество рецептов автора,
        на которого оформлена подписка."""
        return Recipes.objects.filter(author=obj).count()
