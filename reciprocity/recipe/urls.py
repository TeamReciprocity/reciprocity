from django.conf.urls import url
from recipe.views import IngredientAutocomplete, Ingredient

urlpatterns = [
    url(
        r'ingredient-autocomplete/$',
        IngredientAutocomplete.as_view(model=Ingredient, create_field='name'),
        name='ingredient-autocomplete',
    ),
]
