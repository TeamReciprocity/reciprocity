from .models import Ingredient, Recipe, RecipeIngredientRelationship
from dal import autocomplete
from django.forms import inlineformset_factory, modelformset_factory, ModelChoiceField, ModelForm


class IngredientForm(ModelForm):
    ingredient = ModelChoiceField(
        queryset=Ingredient.objects.all(),
        widget=autocomplete.ModelSelect2(url='ingredient-autocomplete')
    )

    class Meta:
        model = Ingredient
        fields = ('__all__')


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'prep_time',
            'cook_time',
            'privacy',
            'directions',
        ]


RecipeIngredientRelationshipFormSet = modelformset_factory(
    RecipeIngredientRelationship,
    fields=('ingredient', 'quantity'),
    widgets={'ingredient': autocomplete.ModelSelect2(url='ingredient-autocomplete')},
    extra=1)
