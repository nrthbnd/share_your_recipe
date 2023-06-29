from django.core.validators import MinValueValidator
from django.db import models
from users.models import User

from .validators import HEX_VALIDATOR


class Ingredients(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        'Название ингредиента',
        max_length=256,
        unique=True,
        help_text='Название ингредиента',
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=100,
        help_text='Единица измерения ингредиента',
    )

    def __str__(self) -> str:
        return f'{self.name} ({self.measurement_unit})'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_unit',
            )
        ]


class Tags(models.Model):
    """Модель тегов."""
    name = models.CharField(
        'Название тега',
        max_length=256,
        unique=True,
        help_text='Название тега рецепта',
    )
    slug = models.SlugField(
        'Слаг тега',
        max_length=100,
        unique=True,
        help_text='Слаг тега',
    )
    color = models.CharField(
        'Код цвета тега в формате HEX',
        unique=True,
        max_length=7,
        validators=[HEX_VALIDATOR],
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipes(models.Model):
    """Модель рецептов."""
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        unique=True,
        help_text='Название рецепта',
    )
    text = models.TextField(
        'Описание рецепта',
        help_text='Описание рецепта',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        help_text='Автор рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления блюда в минутах',
        validators=[MinValueValidator(
            1, 'Время приготовления не может быть менее 1 минуты.')
        ],
        help_text='Время приготовления блюда в минутах',
    )
    image = models.ImageField(
        'Фото блюда',
        upload_to='recipes/images/',
        help_text='Фото блюда',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipesIngredients',
        blank=True,
        verbose_name='Ингредиент',
        related_name='recepies',
    )
    tags = models.ManyToManyField(
        Tags,
        through='RecipesTags',
        blank=True,
        verbose_name='Тег',
        related_name='recepies',
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']


class RecipesIngredients(models.Model):
    """В этой модели всязываются рецепты и ингредиенты."""
    recipe_id = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='id рецепта',
    )
    ingredient_id = models.ForeignKey(
        Ingredients,
        on_delete=models.PROTECT,
        verbose_name='id ингредиента',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        help_text='Количество ингредиента',
        validators=[MinValueValidator(
            1, 'Количество не может быть меньше одиного (ед. изм).')],
    )

    def __str__(self) -> str:
        return f'{self.recipe_id} ({self.ingredient_id}) - {self.amount}.'

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


class RecipesTags(models.Model):
    """В этой модели всязываются рецепты и теги."""
    recipe_id = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='id рецепта',
    )
    tag_id = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        verbose_name='id тега',
    )

    def __str__(self) -> str:
        return f'Рецепту {self.recipe_id} назначен тег {self.tag_id}.'

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'


class Favorites(models.Model):
    """Модель для избранных рецептов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe_id = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='in_favorites',
        verbose_name='id рецепта',
    )

    def __str__(self) -> str:
        return (f'Пользователь {self.user} добавил '
                f'в избранное рецепт {self.recipe_id}.')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe_id', 'user'],
                name='unique_favorite_recipe_user',
            )
        ]


class ShoppingList(models.Model):
    """Модель для списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь',
    )
    recipe_id = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='in_shopping_list',
        verbose_name='id рецепта',
    )

    def __str__(self) -> str:
        return (f'Пользователь {self.user} добавил '
                f'в список покупок рецепт {self.recipe_id}.')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe_id', 'user'],
                name='unique_shopping_list',
            )
        ]
