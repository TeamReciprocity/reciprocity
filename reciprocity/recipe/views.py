from django.shortcuts import render
from dal import autocomplete
from recipe.models import Ingredient

# Create your views here.


class IngredientAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Ingredient.objects.none()
        qs = Ingredient.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
