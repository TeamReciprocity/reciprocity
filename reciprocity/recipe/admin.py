from django.contrib import admin  # pragma: no cover
from .models import Recipe, Ingredient, RecipeIngredientRelationship  # pragma: no cover
from recipe.forms import IngredientForm  # pragma: no cover


class RecipeIngredientRelationshipInline(admin.TabularInline):  # pragma: no cover
    form = IngredientForm
    model = RecipeIngredientRelationship
    extra = 1


class RecipeAdmin(admin.ModelAdmin):  # pragma: no cover
    inlines = (RecipeIngredientRelationshipInline,)


class IngredientAdmin(admin.ModelAdmin):  # pragma: no cover
    pass

admin.site.register(Recipe, RecipeAdmin)  # pragma: no cover

admin.site.register(Ingredient, IngredientAdmin)  # pragma: no cover
