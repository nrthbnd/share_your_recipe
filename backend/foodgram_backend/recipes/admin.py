from django.contrib import admin
from django.contrib.admin import display
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Ingredients, Recipes, ShoppingList, Tags


class RecipesIngredientsInline(admin.TabularInline):
    model = Recipes.ingredients.through
    fields = ('amount', 'ingredients')


class IngredientResource(resources.ModelResource):
    """Испорт данных из файла."""
    class Meta:
        model = Ingredients


class IngredientsAdmin(ImportExportModelAdmin):
    resource_class = IngredientResource
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )
    inlines = (RecipesIngredientsInline,)


admin.site.register(Ingredients, IngredientsAdmin)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'color',
    )


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

    @display(description='Сколько в избранных')
    def in_favorites(self, obj):
        return obj.in_favorites.count()


@admin.register(ShoppingList)
class ShoppingListsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe_id',
    )
