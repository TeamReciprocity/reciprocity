from recipe.models import Ingredient
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
