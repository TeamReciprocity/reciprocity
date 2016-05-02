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
        """Prepare for class test methods."""
        self.no_work_bread = Recipe.objects.get(pk=1)
        self.ants_on_a_log = Recipe.objects.get(pk=2)
        self.michael = self.no_work_bread.author

    def test_title(self):
        """Confirm basic (unrelated) model field is populated correctly."""
        self.assertEqual(self.no_work_bread.title, 'No Work Bread')

    def test_author_relationship(self):
        """Confirm that loaded data is relating properly."""
        self.assertEqual(self.no_work_bread.author, self.michael)

    def test_parent_not_required(self):
        """Confirm parent field may be none."""
        self.assertFalse(self.no_work_bread.parent)


class IngredientTest(TestCase):
    """Test the Ingredient model."""
    fixtures = ['ingredients.json']

    def setUp(self):
        self.yeast = Ingredient.objects.get(pk=4)
        self.ingredient1 = IngredientFactory()

    def test_factory(self):
        """Confirm factory is creating ingredient model instances."""
        self.assertIsInstance(self.ingredient1, Ingredient)

    def test_name(self):
        """Test basic field for model instance."""
        self.assertEqual(self.yeast.name, 'yeast')


class RecipeIngredientTest(TestCase):
    """Test the RecipeIngredientRelationship model."""
    def setUp(self):
        self.recipe_ingredient1 = RecipeIngredientFactory.build()

    def test_factory(self):
        """Confirm factory is creating recipe-ingredient model instances."""
        self.assertIsInstance(self.recipe_ingredient1,
                              RecipeIngredientRelationship)


class Autocomplete(TestCase):
    """Test autocomplete functionality."""
    # load fixtures into test database
    fixtures = ['users.json',
                'ingredients.json',
                'recipes.json',
                'recipeingredientrelationship']

    def setUp(self):
        """Prepare for testing methods."""
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
        """Confirm authenticated client is authenticated."""
        self.assertTrue(self.loggedin)

    def test_autocomplete(self):
        """Confirm autocomplete returning json with completions."""
        url = '/recipe/ingredient-autocomplete/'
        query = '?q=w'
        response = self.auth_client.get(''.join([url, query]))
        expected = ('{"pagination": '
                    '{"more": false}, '
                    '"results": '
                    '[{"text": "water", "id": 2}, '
                    '{"text": "Create \\"w\\"", '
                    '"id": "w", "create_id": true}]}'
                    )
        self.assertEqual(response.content, expected)

#     def test_autocomplete_can_create(self):
#         """Confirm autocomplete can confirm records."""
#         # no tomatoes to begin with
#         queryset = Ingredient.objects.filter(name='tomatoes')
#         self.assertFalse(queryset)
#
#         # get to help the csrf token pop
#         url = '/recipe/ingredient-autocomplete/'
#         query = '?q=tomatoes'
#         get_response = self.auth_client.get(''.join([url, query]))
#
#
#         # use client to post
#         data = {'text': 'tomatoes', id: 200}
#         url = '/recipe/ingredient-autocomplete/'
#         post_response = self.auth_client.post(url, data)
#
#         # assert tomatoes
#         queryset = Ingredient.objects.filter(name='tomatoes')
#         self.assertTrue(queryset)
