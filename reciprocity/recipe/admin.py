from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredientRelationship
from recipe.forms import IngredientForm


class RecipeIngredientRelationshipInline(admin.TabularInline):
    form = IngredientForm
    model = RecipeIngredientRelationship


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientRelationshipInline,)


class IngredientAdmin(admin.ModelAdmin):
    pass

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
