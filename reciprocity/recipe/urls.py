from django.conf.urls import url
from recipe.views import IngredientAutocomplete

urlpatterns = [
    url(
        r'ingredient-autocomplete/$',
        IngredientAutocomplete.as_view(),
        name='ingredient-autocomplete',
    ),
]
