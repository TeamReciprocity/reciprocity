from django.test import TestCase
from factory.django import DjangoModelFactory
from .models import Ingredient, Recipe, RecipeIngredientRelationship


class RecipeFactory(DjangoModelFactory):
    """Instantiate a recipe model instance for testing."""
    class Meta:
        model = Recipe


class IngredientFactory(DjangoModelFactory):
    """Instantiate an ingredient model instance for testing."""
    class Meta:
        model = Ingredient


class RecipeIngredientFactory(DjangoModelFactory):
    """Instantiate a recipe-ingredient model instance for testing."""
    class Meta:
        model = RecipeIngredientRelationship


class RecipeTest(TestCase):
    """Test the Recipe model."""
    def setUp(self):
        self.recipe1 = RecipeFactory.build()

    def test_factory(self):
        """Confirm factory is creating recipe model instances."""
        self.assertIsInstance(self.recipe1, Recipe)


class IngredientTest(TestCase):
    """Test the Ingredient model."""
    def setUp(self):
        self.ingredient1 = IngredientFactory.build()

    def test_factory(self):
        """Confirm factory is creating ingredient model instances."""
        self.assertIsInstance(self.ingredient1, Ingredient)


class RecipeIngredientTest(TestCase):
    """Test the RecipeIngredientRelationship model."""
    def setUp(self):
        self.recipe_ingredient1 = RecipeIngredientFactory.build()

    def test_factory(self):
        """Confirm factory is creating recipe-ingredient model instances."""
        self.assertIsInstance(self.recipe_ingredient1,
                              RecipeIngredientRelationship)
