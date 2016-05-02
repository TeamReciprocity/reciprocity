from django.conf.urls import url
from recipe.views import IngredientAutocomplete, Ingredient
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(
        r'ingredient-autocomplete/$',
        login_required(IngredientAutocomplete.as_view(model=Ingredient,
                                                      create_field='name')),
        name='ingredient-autocomplete',
    ),
]
