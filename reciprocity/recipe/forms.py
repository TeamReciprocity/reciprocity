from .models import Ingredient, Recipe
from dal import autocomplete
from django import forms


class IngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        widget=autocomplete.ModelSelect2(url='ingredient-autocomplete')
    )

    class Meta:
        model = Ingredient
        fields = ('__all__')


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'prep_time',
            'cook_time',
            'privacy',
            'directions',
            'ingredients',
        ]
