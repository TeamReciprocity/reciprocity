from dal import autocomplete
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import RecipeIngredientRelationshipFormSet, RecipeForm
from .models import Ingredient, Recipe, RecipeIngredientRelationship


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


def edit_recipe(request, **kwargs):
    """Handle edit of existing recipe."""
    template = 'recipe/add-recipe.html'
    pk = kwargs.get('pk')
    recipe = Recipe.objects.get(pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = RecipeIngredientRelationshipFormSet(request.POST, prefix='ingredient_form')
        if formset.is_valid() and form.is_valid():
            for ingredient in formset.cleaned_data:
                # import pdb; pdb.set_trace()
                if ingredient:
                    if ingredient['id']:
                        rel_id = RecipeIngredientRelationship.objects.get(id=ingredient['id'].id)
                        # update relationship
                        pass
                    else:
                        new = RecipeIngredientRelationship(recipe=recipe,
                                               quantity=ingredient['quantity'],
                                               ingredient=ingredient['ingredient'])
                        new.save()
            return HttpResponseRedirect('/')
    else:
        recipe_form = RecipeForm(instance=recipe)
        formset = RecipeIngredientRelationshipFormSet(queryset=recipe.ingredients_in_recipe.all(), prefix='ingredient_form')

    return render(request, template, {'formset': formset, 'recipe_form': recipe_form})
