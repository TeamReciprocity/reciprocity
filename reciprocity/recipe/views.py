from dal import autocomplete
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import RecipeIngredientRelationshipFormSet, RecipeForm
from .models import Ingredient, Recipe, RecipeIngredientRelationship


class MyRecipesListView(ListView):
    def get_queryset(self):
        """Return authored recipes."""
        return Recipe.objects.filter(author=self.request.user)


class RecipeDetailView(DetailView):
    def get_object(self, queryset=None):
        """Secure private recipes."""
        recipe = super(DetailView, self).get_object()
        if recipe.privacy != 'pu' and self.request.user != recipe.author:
            raise Http404
        return recipe


class IngredientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Ingredient.objects.none()
        qs = Ingredient.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = RecipeIngredientRelationshipFormSet(request.POST, prefix='ingredient_form')
        if formset.is_valid() and form.is_valid():
            form.instance.author = request.user
            form.save()
            for ingredient in formset.cleaned_data:
                if ingredient:
                    new = RecipeIngredientRelationship(recipe=form.instance,
                                                       quantity=ingredient['quantity'],
                                                       ingredient=ingredient['ingredient'])
                    new.save()
            return HttpResponseRedirect('/')
    else:
        recipe_form = RecipeForm()
        formset = RecipeIngredientRelationshipFormSet(
            queryset=RecipeIngredientRelationship.objects.none(),
            prefix='ingredient_form'
        )
    return render(request,
                  'recipe/add-recipe.html',
                  {'recipe_form': recipe_form,
                   'formset': formset})
