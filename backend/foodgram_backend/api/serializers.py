import base64

from django.core.files.base import ContentFile
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, serializers
from rest_framework.fields import SerializerMethodField

from recipes.models import (Favorites, Ingredients, Recipes,
                            RecipesIngredients, ShoppingList, Tags)
from users.serializers import CustomUserSerializer


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class RecipesIngredientsSerializer(serializers.Serializer):
    """Получение объекта amount таблицы RecipesIngredients."""
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField()

    class Meta:
        model = RecipesIngredients
        fields = ('id', 'amount')


class CustomImageField(serializers.ImageField):
    """Декодирует строку base64 в картинку и сохраняет ее как файл."""
    def to_internal_value(self, data):
        if 'data' in data and ';base64' in data:
            format, imagestr = data.split(';base64,')
            extension = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imagestr),
                name='temp.' + extension
            )
            return super().to_internal_value(data)


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


class RecipesReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра рецептов."""
    tags = TagsSerializer(many=True)
    author = CustomUserSerializer()
    is_favorited = SerializerMethodField(method_name='get_favorited')
    ingredients = SerializerMethodField(method_name='get_ingredients')
    is_in_shopping_cart = SerializerMethodField(
        method_name='get_shopping_cart')
    image = CustomImageField()

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
        read_only_fields = ('__all__',)

    def get_favorited(self, obj):
        """Возвращает True/False об Избранном для пользователя,
        отправляющего запрос."""
        user = self.context['request'].user
        return Favorites.objects.filter(
            user=user, recipe_id=obj.id).exists()

    def get_ingredients(self, obj):
        """Получает значения полей из модели Ингредиентов
        и значение amount из общей таблицы RecipesIngredients."""
        recipe = obj
        ingredients = recipe.ingredients.values(
            'id', 'name', 'measurement_unit',
            amount=F('recipesingredients__amount')
        )
        return ingredients

    def get_shopping_cart(self, obj):
        """Возвращает True/False о добавлении в состав корзины для
        пользователя, отправляющего запрос."""
        user = self.context['request'].user
        recipe = obj.id
        return ShoppingList.objects.filter(
            user=user, recipe_id=recipe).exists()


class RecipesWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления и частичного изменения рецептов."""
    ingredients = RecipesIngredientsSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(), many=True)
    image = CustomImageField()
    author = CustomUserSerializer(read_only=True,)

    class Meta:
        model = Recipes
        fields = ('ingredients', 'tags', 'image', 'name', 'text',
                  'cooking_time', 'author')

    def validate_ingredients(self, value):
        """Проверка создания ингридиентов."""
        if not value:
            raise exceptions.ValidationError(
                'Необходимо добавить ингридиент.')

        ingredients = [ingredient['id'] for ingredient in value]
        for item in ingredients:
            if ingredients.count(item) > 1:
                raise exceptions.ValidationError(
                    'Этот ингредиент уже добавлен в рецепт.')
        return value

    def validate_tags(self, value):
        """Проверка создания тегов."""
        if not value:
            raise exceptions.ValidationError(
                'Необходимо добавить тег.')
        return value           

    def create(self, validated_data):
        """Создает рецепт и добавляет в связанные модели рецептов
        и ингридиентов, рецептов и тегов новые поля."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipes.objects.create(**validated_data)
        recipe.tags.set(tags)

        RecipesIngredients.objects.bulk_create([RecipesIngredients(
            ingredient_id=get_object_or_404(Ingredients, pk=ingredient['id']),
            amount=ingredient['amount'],
            recipe_id=recipe,
            ) for ingredient in ingredients]
        )

        return recipe

    def update(self, instance, validated_data):
        """Проверяет, есть ли в модели объект ингридиентов и тегов
        и заменяет их."""
        if 'ingredients' in validated_data:
            instance.ingredients.clear()
            ingredients = validated_data.pop('ingredients')
        if 'tags' in validated_data:
            instance.tags.clear()
            tags = validated_data.pop('tags')

        instance = super().update(instance, validated_data)
        return self.add_ingredient_and_tag_in_recipe(
            instance,
            ingredients=ingredients,
            tags=tags)

    def to_representation(self, instance):
        """Преобразует объект модели в словарь. Создает экземпляр
        RecipesReadSerializer и возвращает данные сериализатора."""
        request = self.context.get('request')
        context = {'request': request}
        return RecipesReadSerializer(instance, context=context).data


class RecipesMajorSerializer(serializers.ModelSerializer):
    """Поля для favorite & shopping_cart."""
    image = CustomImageField()

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('author',)
