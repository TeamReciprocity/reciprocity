from django.conf.urls import url
from .views import AddRecipe, IngredientAutocomplete, Ingredient
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(
        r'ingredient-autocomplete/$',
        login_required(IngredientAutocomplete.as_view(model=Ingredient,
                                                      create_field='name')),
        name='ingredient-autocomplete',
    ),
    url(r'add/$', login_required(AddRecipe.as_view()), name='add-recipe'),
]
