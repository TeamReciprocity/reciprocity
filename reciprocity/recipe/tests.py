from django.conf import settings
from django.test import Client, TestCase
from factory.django import DjangoModelFactory
from .models import Ingredient, Recipe, RecipeIngredientRelationship
from .forms import RecipeIngredientRelationshipFormSet, IngredientForm
from .forms import RecipeForm
from django.forms import formsets
from datetime import datetime
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


class RecipeModelTest(TestCase):
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


class IngredientModelTest(TestCase):
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


class RecipeIngredientModelTest(TestCase):
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


class TestView(TestCase):
    """Generic class for testing views."""
    def setUp(self):
        """Provide user and client authenticated as user."""
        self.user = UserFactory()
        self.user.set_password(PASSWORD)
        self.user.save()
        self.client = Client()
        self.client.login(username=self.user, password=PASSWORD)


class ViewMyFavorites(TestView):
    def setUp(self):
        super(ViewMyFavorites, self).setUp()
        self.favorite_recipe = RecipeFactory()
        self.favorite_recipe.favorite_of.add(self.user.profile)
        self.unfavorited_recipe = RecipeFactory()

    def test_including(self):
        """Confirm view lists user's favorite recipes."""
        response = self.client.get('/recipe/view/favorites/')
        self.assertIn(str(self.favorite_recipe), str(response.content))

    def test_excluding(self):
        """Confirm view excludes unfavorited recipes."""
        response = self.client.get('/recipe/view/favorites/')
        self.assertNotIn(str(self.unfavorited_recipe), str(response.content))


class ViewMyRecipes(TestView):
    def setUp(self):
        super(ViewMyRecipes, self).setUp()
        self.authored_recipe = RecipeFactory(author=self.user)
        self.unauthored_recipe = RecipeFactory(author=UserFactory())

    def test_including(self):
        """Confirm view lists user's recipes."""
        response = self.client.get('/recipe/view/my_recipes/')
        self.assertIn(str(self.authored_recipe), str(response.content))

    def test_excluding(self):
        """Confirm view excludes non-authored recipes."""
        response = self.client.get('/recipe/view/my_recipes/')
        self.assertNotIn(str(self.unauthored_recipe), str(response.content))


class ViewRecipe(TestView):
    def setUp(self):
        """Prepare for test methods."""
        super(ViewRecipe, self).setUp()
        non_author = UserFactory(username='non-author')
        non_author.set_password(PASSWORD)
        non_author.save()
        self.non_author_client = Client()
        self.non_author_client.login(username=non_author.username,
                                     password=PASSWORD)
        self.public_recipe = RecipeFactory(author=self.user, privacy='pu')
        self.private_recipe = RecipeFactory(author=self.user, privacy='pr')

    def test_authored_public(self):
        """Confirm author can view public authored recipe."""
        url = ''.join(['/recipe/view/',
                       str(self.public_recipe.pk),
                       '/'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_authored_private(self):
        """Confirm author can view private authored recipe."""
        url = ''.join(['/recipe/view/',
                       str(self.private_recipe.pk),
                       '/'])
        response = self.client.get(url)
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
        expected = ['"text": "water"', '"id": 2', ]
        for item in expected:
            self.assertIn(str(item), str(response.content))


class CreateRecipe(TestCase):
    """Test create view Functionality."""
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
        self.loggedout_client = Client()

    def test_auth_200(self):
        """Verify logged in user can get to create recipe page."""
        response = self.author_client.get('/recipe/add/')
        self.assertEquals(response.status_code, 200)

    def test_unauth_302(self):
        """Verify logged out user is redirected to
        login page when attempting to create a recipe."""
        response = self.loggedout_client.get('/recipe/add/')
        self.assertEquals(response.status_code, 302)

    def test_forms_available(self):
        """Verify some of the expected forms are on the page."""
        response = self.author_client.get('/recipe/add/')
        self.assertIn('input id="id_title"', str(response.content))
        self.assertIn('id="id_prep_time"', str(response.content))
        self.assertIn('id="id_cook_time"', str(response.content))
        self.assertIn('id="id_privacy"', str(response.content))
        self.assertIn('id="id_description"', str(response.content))

    def test_formset_autocomplete(self):
        """Verify the ingredient form is pointing the autocomplete url."""
        response = self.author_client.get('/recipe/add/')
        self.assertIn('data-autocomplete-light-url="/recipe/ingredient-autocomplete/"', str(response.content))


class EditRecipe(TestCase):
    """Test create view Functionality."""
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
        self.loggedout_client = Client()
        self.public_recipe = RecipeFactory(author=author, privacy='pu')
        self.public_recipe.save()
        relationship1 = RecipeIngredientFactory()
        relationship1.recipe = self.public_recipe
        relationship2 = RecipeIngredientFactory()
        relationship2.recipe = self.public_recipe
        relationship1.save()
        relationship2.save()
        self.pk = self.public_recipe.pk

    def test_auth_200(self):
        """Verify logged in user can get to create recipe page."""
        response = self.author_client.get('/recipe/edit/{}/'.format(self.pk))
        self.assertEquals(response.status_code, 200)

    def test_unauth_302(self):
        """Verify logged out user is redirected to
        login page when attempting to create a recipe."""
        response = self.loggedout_client.get('/recipe/edit/{}/'.format(self.pk))
        self.assertEquals(response.status_code, 302)

    def test_forms_available(self):
        """Verify some of the expected forms are on the page."""
        response = self.author_client.get('/recipe/edit/{}/'.format(self.pk))
        self.assertIn('input id="id_title"', str(response.content))
        self.assertIn('id="id_prep_time"', str(response.content))
        self.assertIn('id="id_cook_time"', str(response.content))
        self.assertIn('id="id_privacy"', str(response.content))
        self.assertIn('id="id_description"', str(response.content))

    def test_formset_autocomplete(self):
        """Verify the ingredient form is pointing the autocomplete url."""
        response = self.author_client.get('/recipe/edit/{}/'.format(self.pk))
        self.assertIn('data-autocomplete-light-url="/recipe/ingredient-autocomplete/"', str(response.content))


class FormsTest(TestCase):
    """Test Form Creation."""
    def setUp(self):
        """Prepare for test methods."""
        self.formset = RecipeIngredientRelationshipFormSet(
            queryset=RecipeIngredientRelationship.objects.none())
        author = UserFactory(username='author')
        author.set_password(PASSWORD)
        author.save()
        self.public_recipe = RecipeFactory(author=author, privacy='pu')
        self.public_recipe.save()
        relationship1 = RecipeIngredientFactory()
        relationship1.recipe = self.public_recipe
        relationship2 = RecipeIngredientFactory()
        relationship2.recipe = self.public_recipe
        relationship1.save()
        relationship2.save()
        self.formset_filled = RecipeIngredientRelationshipFormSet(
            queryset=RecipeIngredientRelationship.objects.filter(recipe=self.public_recipe))
        self.recipe_form = RecipeForm()
        self.ingredient_form = IngredientForm()

    def test_formset_0_initial(self):
        """Verify empty formset initializes with 0 forms."""
        self.assertEquals(self.formset.initial_form_count(), 0)

    def test_formset_1_extra(self):
        """Verify one additional form is added to the formset."""
        self.assertEquals(len(self.formset.extra_forms), 1)

    def test_formset_based_on_recipe_ingredient_count(self):
        """Verify populated formset has forms for each ingredient."""
        self.assertEquals(len(self.public_recipe.ingredients.all()),
                          self.formset_filled.initial_form_count())

    def test_recipe_form_fields(self):
        """Verify recipe form does not show specific fields."""
        self.assertRaises(KeyError, lambda: self.recipe_form['author'])
        self.assertRaises(KeyError, lambda: self.recipe_form['parent'])
        self.assertRaises(KeyError, lambda: self.recipe_form['created'])

    def test_ingredient_form_fields(self):
        """Verify recipe form shows all ingredients."""
        count = 0
        for option in self.ingredient_form.fields['ingredient'].choices:
            count += 1
        self.assertEquals(count, 3)


class ModelTests(TestCase):
    """Test recipe models and associated models."""
    def setUp(self):
        """Prepare for test methods."""
        self.author = UserFactory(username='author')
        self.author.set_password(PASSWORD)
        self.author.save()
        self.public_recipe = RecipeFactory(author=self.author, privacy='pu')
        self.public_recipe.save()
        self.relationship1 = RecipeIngredientFactory()
        self.relationship1.recipe = self.public_recipe
        self.relationship1.quantity = '5 Cups'
        relationship2 = RecipeIngredientFactory()
        relationship2.recipe = self.public_recipe
        self.relationship1.save()
        relationship2.save()

    def test_recipe_title(self):
        """Verify recipe title exists."""
        self.assertTrue(self.public_recipe.title)

    def test_recipe_create_date(self):
        """Verify recipe has a created date after it being saved."""
        self.assertTrue(self.public_recipe.created)

    def test_recipe_create_date_type(self):
        """Verify datetime object exists in the recipe model after being saved."""
        recipe2 = Recipe(author=self.author, title='test', description='test')
        self.assertFalse(recipe2.created)
        recipe2.save()
        self.assertTrue(recipe2.created)

    def test_recipe_datetime_object(self):
        """Verify datetime property is the type datetime."""
        self.assertIsInstance(self.public_recipe.created, datetime)

    def test_recipe_privacy_default(self):
        """Verify that public is the default privacy setting."""
        self.assertEquals(self.public_recipe.privacy, 'pu')

    def test_recipe_has_ingredients(self):
        """Verify that the setup recipe has ingredients,
           seen through the through table."""
        self.assertTrue(self.public_recipe.ingredients)

    def test_ingredient_has_name(self):
        """Test stringing an ingredient displays name."""
        pasta = Ingredient(name='pasta')
        self.assertEquals(str(pasta), 'pasta')

    def test_relationship_exists(self):
        """Verify relationship points to ingredient and recipe."""
        self.assertIsInstance(self.relationship1.ingredient, Ingredient)
        self.assertIsInstance(self.relationship1.recipe, Recipe)

    def test_relationship_quantity(self):
        self.assertEquals(self.relationship1.quantity, '5 Cups')


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
