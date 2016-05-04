from django.conf import settings
from django.test import Client, TestCase
from factory.django import DjangoModelFactory
from .models import Ingredient, Recipe, RecipeIngredientRelationship

import factory

PASSWORD = 'this is the password'


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
    title = factory.Faker('name')


class IngredientFactory(DjangoModelFactory):
    """Instantiate an ingredient model instance for testing."""
    class Meta:
        model = Ingredient

    name = factory.Faker('name')


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

    def test_variant_relationship(self):
        """Confirm a new recipe can be a variant."""
        self.variant = RecipeFactory(title='Fuzzy Ants on a log',
                                     description='A zesty take on an old classic',
                                     directions='Throw it all together, carefully.',
                                     parent=self.ants_on_a_log)
        self.assertEqual(self.variant, self.ants_on_a_log.variations.first())
        self.assertEqual(self.variant.parent, self.ants_on_a_log)


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
    fixtures = ['users.json',
                'ingredients.json',
                'recipes.json',
                'recipeingredientrelationship']

    def setUp(self):
        self.recipe_ingredient1 = RecipeIngredientFactory.build()
        self.no_work_bread = Recipe.objects.get(pk=1)
        self.ants_on_a_log = Recipe.objects.get(pk=2)
        self.salt = Ingredient.objects.get(name='salt')
        self.flour = Ingredient.objects.get(name='flour, white')

    def test_factory(self):
        """Confirm factory is creating recipe-ingredient model instances."""
        self.assertIsInstance(self.recipe_ingredient1,
                              RecipeIngredientRelationship)

    def test_recipe_to_ingredient(self):
        """Confirm a given recipe has a relationship to said ingredient."""
        thru_table = RecipeIngredientRelationship.objects.filter(
            recipe=self.no_work_bread
        )
        self.assertTrue(thru_table.filter(ingredient=self.salt))
        self.assertEqual(self.no_work_bread.ingredients.first(), self.flour)


class ViewMyRecipes(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.set_password(PASSWORD)
        self.user.save()
        self.client = Client()
        self.client.login(username=self.user, password=PASSWORD)
        self.authored_recipe = RecipeFactory(author=self.user)
        self.unauthored_recipe = RecipeFactory(author=UserFactory())

    def test_including(self):
        """Confirm view lists user's recipes."""
        response = self.client.get('/recipe/view/my_recipes/')
        self.assertIn(str(self.authored_recipe), response.content)

    def test_excluding(self):
        """Confirm view excludes non-authored recipes."""
        response = self.client.get('/recipe/view/my_recipes/')
        self.assertNotIn(str(self.unauthored_recipe), response.content)


class ViewRecipe(TestCase):
    def setUp(self):
        """Prepare for test methods."""
        author = UserFactory(username='author')
        author.set_password(PASSWORD)
        author.save()
        non_author = UserFactory(username='non-author')
        non_author.set_password(PASSWORD)
        non_author.save()
        self.author_client = Client()
        self.loggedin = self.author_client.login(username=author.username,
                                                 password=PASSWORD)
        self.non_author_client = Client()
        self.non_author_client.login(username=non_author.username,
                                     password=PASSWORD)
        self.public_recipe = RecipeFactory(author=author, privacy='pu')
        self.private_recipe = RecipeFactory(author=author, privacy='pr')

    def test_client_authorized(self):
        """Confirm client is logged in."""
        self.assertTrue(self.loggedin)

    def test_authored_public(self):
        """Confirm author can view public authored recipe."""
        url = ''.join(['/recipe/view/',
                       str(self.public_recipe.pk),
                       '/'])
        response = self.author_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_authored_private(self):
        """Confirm author can view private authored recipe."""
        url = ''.join(['/recipe/view/',
                       str(self.private_recipe.pk),
                       '/'])
        response = self.author_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unauthored_public(self):
        """Confirm non-author can view public recipe."""
        url = ''.join(['/recipe/view/',
                       str(self.public_recipe.pk),
                       '/'])
        response = self.non_author_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unauthored_private(self):
        """Confirm non-author cannot view private recipe."""
        url = ''.join(['/recipe/view/',
                       str(self.private_recipe.pk),
                       '/'])
        response = self.non_author_client.get(url)
        self.assertEqual(response.status_code, 404)


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
        self.auth_user.set_password(PASSWORD)
        self.auth_user.save()
        self.auth_client = Client()
        self.loggedin = self.auth_client.login(username=username,
                                               password=PASSWORD)
        self.unauth_client = Client()

    def test_authenticated(self):
        """Confirm authenticated client is authenticated."""
        self.assertTrue(self.loggedin)

    def test_autocomplete_unauthenticated(self):
        """Confirm unauthenticated client can not see autocomplete view."""
        url = '/recipe/ingredient-autocomplete/'
        query = '?q=w'
        response = self.unauth_client.get(''.join([url, query]))
        self.assertEqual(response.status_code, 302)

    def test_autocomplete_authenticated(self):
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
