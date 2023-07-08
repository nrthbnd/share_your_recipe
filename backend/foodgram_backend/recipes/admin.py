from django.conf import settings
from django.contrib import admin
from django.contrib.admin import display
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (Ingredients, Recipes, RecipesIngredients,
                     RecipesTags, ShoppingList, Tags)


class RecipesIngredientsInline(admin.TabularInline):
    model = RecipesIngredients


class RecipesTagsInline(admin.TabularInline):
    model = RecipesTags


class IngredientResource(resources.ModelResource):
    """Испорт данных из файла."""
    class Meta:
        model = Ingredients


class IngredientsAdmin(ImportExportModelAdmin):
    resource_class = IngredientResource
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = settings.EMPTY_VALUE


admin.site.register(Ingredients, IngredientsAdmin)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
        'color',
    )
    search_fields = ('name', 'slug', 'color')
    list_filter = ('name', 'slug', 'color')
    empty_value_display = settings.EMPTY_VALUE


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'in_favorites',
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    readonly_fields = (
        'in_favorites',
    )
    inlines = (RecipesIngredientsInline, RecipesTagsInline,)
    empty_value_display = settings.EMPTY_VALUE

    @display(description='Сколько в избранных')
    def in_favorites(self, obj):
        return obj.in_favorites.count()


@admin.register(RecipesIngredients)
class RecipesIngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe_id',
        'ingredient_id',
        'amount',
    )
    empty_value_display = settings.EMPTY_VALUE


@admin.register(ShoppingList)
class ShoppingListsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe_id',
    )
    empty_value_display = settings.EMPTY_VALUE
