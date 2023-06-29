from django.http import HttpResponse
from django.db.models import Sum

from recipes.models import ShoppingList, RecipesIngredients


def create_shopping_list_file(user):
    """Создает файл с суммированным перечнем и количеством
    необходимых ингредиентов."""
    if not user.shopping_cart.exists():
        return None

    products = ShoppingList.objects.filter(user=user)
    recipes_list = [product.recipe_id for product in products]

    shopping_list = RecipesIngredients.objects.filter(
        recipe_id__in=recipes_list).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(total_amount=Sum('amount'))

    content = 'Ваш список покупок:\n\n'
    for item in shopping_list:
        name = item['ingredient__name']
        amount = item['total_amount']
        content += f'{name}: {amount}\n'

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.txt"')
    response.write(content)

    return response
