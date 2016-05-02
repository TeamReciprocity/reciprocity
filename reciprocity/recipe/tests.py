from django.conf import settings
from django.test import Client, TestCase
from factory.django import DjangoModelFactory
from .models import Ingredient, Recipe, RecipeIngredientRelationship

import factory


class UserFactory(DjangoModelFactory):
    """Instantiate a user model instance for testing."""
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker('first_name')


class RecipeFactory(DjangoModelFactory):
    """Instantiate a recipe model instance for testing."""
    class Meta:
        model = Recipe

    author = factory.SubFactory(UserFactory)


class IngredientFactory(DjangoModelFactory):
    """Instantiate an ingredient model instance for testing."""
    class Meta:
        model = Ingredient


class RecipeIngredientFactory(DjangoModelFactory):
    """Instantiate a recipe-ingredient model instance for testing."""
    class Meta:
        model = RecipeIngredientRelationship

    recipe = factory.SubFactory(RecipeFactory)
    ingredient = factory.SubFactory(IngredientFactory)


class RecipeTest(TestCase):
    """Test the Recipe model."""
    fixtures = ['users.json', 'recipes.json']

    def setUp(self):
        self.no_work_bread = Recipe.objects.get(pk=1)
        self.ants_on_a_log = Recipe.objects.get(pk=2)
        self.michael = self.no_work_bread.author

    def test_title(self):
        self.assertEqual(self.no_work_bread.title, 'No Work Bread')

    def test_author_relationship(self):
        self.assertEqual(self.no_work_bread.author, self.michael)

    def test_parent_not_required(self):
        self.assertFalse(self.no_work_bread.parent)


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


class Autocomplete(TestCase):
    fixtures = ['users.json',
                'ingredients.json',
                'recipes.json',
                'recipeingredientrelationship']

    def setUp(self):
        self.auth_user = UserFactory()
        username = self.auth_user.username
        password = 'this is the password'
        self.auth_user.set_password(password)
        self.auth_user.save()
        self.auth_client = Client()
        self.loggedin = self.auth_client.login(username=username,
                                               password=password)
        self.unauth_client = Client()

    def test_authenticated(self):
        self.assertTrue(self.loggedin)

    def test_autocomplete(self):
        url = '/recipe/ingredient-autocomplete/'
        query = '?q=w'
        response = self.auth_client.get(''.join([url, query]))
        expected = ('{"pagination":'
                    ' {"more": false},'
                    ' "results":'
                    ' [{"text": "white flour", "id": 1},'
                    ' {"text": "water", "id": 2},'
                    ' {"text": "Create \\"w\\"",'
                    ' "id": "w", "create_id": true}]}'
                    )
        self.assertEqual(response.content, expected)
