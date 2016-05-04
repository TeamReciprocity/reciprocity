from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from .models import Recipe
from .views import add_recipe, IngredientAutocomplete, Ingredient

urlpatterns = [
    url(r'^ingredient-autocomplete/$',
        login_required(IngredientAutocomplete.as_view(model=Ingredient,
                                                      create_field='name')),
        name='ingredient-autocomplete',),
    url(r'^add/$', login_required(add_recipe), name='add-recipe'),
    url(r'^view/(?P<pk>[0-9]+)/$',
        login_required(DetailView.as_view(model=Recipe,
                                          template_name='recipe/view-recipe.html')),
        name='view-recipe'),
    url(r'^edit/(?P<pk>[0-9]+)/$',
        login_required(DetailView.as_view(model=Recipe,
                                          template_name='recipe/edit-recipe.html')),
        name='edit-recipe'),
    url(r'^vary/(?P<pk>[0-9]+)/$',
        login_required(DetailView.as_view(model=Recipe,
                                          template_name='recipe/vary-recipe.html')),
        name='vary-recipe'),
]
