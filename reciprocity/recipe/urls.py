from django.conf.urls import url
from .views import add_recipe, IngredientAutocomplete, Ingredient, edit_recipe
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(
        r'ingredient-autocomplete/$',
        login_required(IngredientAutocomplete.as_view(model=Ingredient,
                                                      create_field='name')),
        name='ingredient-autocomplete',
    ),
    # url(r'add/$', login_required(AddRecipe.as_view()), name='add-recipe'),
    url(r'add/$', login_required(add_recipe), name='add-recipe'),
    url(r'edit/(?P<pk>[0-9]+)', login_required(edit_recipe), name='edit-recipe')
]
