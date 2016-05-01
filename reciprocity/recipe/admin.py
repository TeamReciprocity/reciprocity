from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredientRelationship


# Register your models here.
class RecipeIngredientRelationshipInline(admin.TabularInline):
    model = RecipeIngredientRelationship
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientRelationshipInline,)


class IngredientAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientRelationshipInline,)


class RecipeIngredientRelationshipAdmin(admin.ModelAdmin):
    pass


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredientRelationship,
                    RecipeIngredientRelationshipAdmin)
