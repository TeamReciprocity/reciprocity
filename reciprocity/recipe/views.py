from dal import autocomplete
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .forms import RecipeIngredientRelationshipFormSet, RecipeForm
from .models import Ingredient, Recipe, RecipeIngredientRelationship


class FavoriteRecipesView(ListView):
    def get_queryset(self):
        """Return favorited recipes."""
        return Recipe.objects.filter(favorite_of=self.request.user.profile)


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
        qs = Ingredient.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


def add_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        formset = RecipeIngredientRelationshipFormSet(request.POST,
                                                      prefix='ingredient_form')
        if formset.is_valid() and recipe_form.is_valid():
            recipe_form.instance.author = request.user
            recipe_form.save()
            for ingredient in formset.cleaned_data:
                if ingredient:
                    new = RecipeIngredientRelationship(recipe=recipe_form.instance,
                                                       quantity=ingredient['quantity'],
                                                       ingredient=ingredient['ingredient'])
                    new.save()
            return HttpResponseRedirect('/')
    else:
        recipe_form = RecipeForm()
        formset = RecipeIngredientRelationshipFormSet(
            queryset=RecipeIngredientRelationship.objects.none(),
            prefix='ingredient_form')
    return render(request,
                  'recipe/add-edit-vary.html',
                  {'recipe_form': recipe_form,
                   'formset': formset,
                   'page_title': 'Add Recipe'})


def edit_recipe(request, **kwargs):
    """Handle edit of existing recipe."""
    template = 'recipe/add-edit-vary.html'
    pk = kwargs.get('pk')
    recipe = Recipe.objects.get(pk=pk)
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
        formset = RecipeIngredientRelationshipFormSet(request.POST,
                                                      prefix='ingredient_form')
        if formset.is_valid() and recipe_form.is_valid():
            recipe_form.save()
            for ingredient in formset.cleaned_data:
                if ingredient:
                    if ingredient['id']:
                        relationship = RecipeIngredientRelationship.objects.get(id=ingredient['id'].id)
                        relationship.quantity = ingredient['quantity']
                        relationship.ingredient = ingredient['ingredient']
                        relationship.save()
                    else:
                        new = RecipeIngredientRelationship(recipe=recipe,
                                                           quantity=ingredient['quantity'],
                                                           ingredient=ingredient['ingredient'])
                        new.save()
            return HttpResponseRedirect('/')
    else:
        recipe_form = RecipeForm(instance=recipe)
        formset = RecipeIngredientRelationshipFormSet(queryset=recipe.ingredients_in_recipe.all(), prefix='ingredient_form')
    return render(request, template, {'formset': formset,
                                      'recipe_form': recipe_form,
                                      'page_title': 'Edit Recipe'})


def vary_recipe(request, **kwargs):
    template = 'recipe/add-edit-vary.html'
    pk = kwargs.get('pk')
    parent_recipe = Recipe.objects.get(pk=pk)
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        formset = RecipeIngredientRelationshipFormSet(request.POST,
                                                      prefix='ingredient_form')
        if formset.is_valid() and recipe_form.is_valid():
            recipe_form.instance.author = request.user
            recipe_form.instance.parent = parent_recipe
            recipe_form.save()
            for ingredient in formset.cleaned_data:
                if ingredient:
                    new = RecipeIngredientRelationship(recipe=recipe_form.instance,
                                                       quantity=ingredient['quantity'],
                                                       ingredient=ingredient['ingredient'])
                    new.save()
            cur = parent_recipe
            while cur:
                recipe_form.instance.ancestors.add(cur)
                recipe_form.save()
                if cur.parent:
                    cur = cur.parent
                else:
                    break
            return HttpResponseRedirect('/')
    else:
        recipe_form = RecipeForm(instance=parent_recipe)
        formset = RecipeIngredientRelationshipFormSet(queryset=parent_recipe.ingredients_in_recipe.all(), prefix='ingredient_form')
    return render(request, template, {'formset': formset,
                                      'recipe_form': recipe_form,
                                      'page_title': 'Vary Recipe'})
