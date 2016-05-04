from django.conf import settings
from django.test import Client, TestCase
from factory.django import DjangoModelFactory
from django.views.decorators.csrf import csrf_exempt
from .tests import (UserFactory, IngredientFactory,
                    RecipeFactory, RecipeIngredientFactory)
from .models import Ingredient, Recipe, RecipeIngredientRelationship
import factory


class CreateRecipeForm(TestCase):
    """Test case for creating recipes through form."""

    def setUp(self):
        """Create authenticated users to test views that need login."""
        pass
        # create users and log them in

    # test that logged in users can post to create page to make new recipes.
