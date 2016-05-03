from dal import autocomplete
from django.views.generic.edit import CreateView
from .forms import RecipeIngredientRelationshipFormSet, RecipeForm
from .models import Ingredient, Recipe


class IngredientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Ingredient.objects.none()
        qs = Ingredient.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class AddRecipe(CreateView):
    template_name = 'recipe/add-recipe.html'
    # TODO: why both model and form class??
    model = Recipe
    form_class = RecipeForm
    success_url = '/'

    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        form.instance.save()
        return super(AddRecipe, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        recipe_form = self.get_form(form_class)
        recipe_ingredient_relationship_form = RecipeIngredientRelationshipFormSet()
        return self.render_to_response(
            self.get_context_data(recipe_form=recipe_form,
                                  recipe_relationship_ingredient_form=recipe_ingredient_relationship_form))

