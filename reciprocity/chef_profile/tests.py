"""Test ChefProfile model."""
from __future__ import unicode_literals
from django.conf import settings
from django.test import TestCase, Client
from django.db.models import QuerySet, Manager
from recipe.tests import RecipeFactory, IngredientFactory
from .models import ChefProfile
from django.contrib.auth.models import Permission
import factory

USER_BATCH_SIZE = 20
MODELS = ['recipe', 'ingredient', 'recipeingredientrelationship']
ACTIONS = ['add', 'change', 'delete']
PERMS = ['_'.join((action, model)) for action in ACTIONS for model in MODELS]
PERMS += ['change_user', 'change_chefprofile']


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for User model in tests."""

    class Meta:
        """Establish User model as the product of this factory."""

        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    username = factory.LazyAttribute(
        lambda obj: ''.join((obj.first_name, obj.last_name)))
    password = factory.PostGenerationMethodCall('set_password', 'secret')


class BuiltUserCase(TestCase):
    """Single user not saved to database, testing functionality of handlers."""

    def setUp(self):
        """Set up user stub."""
        self.user = UserFactory.build()

    def test_user_not_saved(self):
        """Make sure set up user has not been saved yet."""
        self.assertIsNone(self.user.id)

    def test_init_chef_profile(self):
        """Test that ChefProfile created on save."""
        profile = ChefProfile(user=self.user)
        self.assertIs(profile, self.user.profile)


class SingleUserCase(TestCase):
    """Set up single user for tests."""

    def setUp(self):
        """Create a user for testing, add same permissions assigned in 
        handlers.py.
        """
        self.user = UserFactory.create()
        self.recipe = RecipeFactory.create()
        self.ingredient1 = IngredientFactory.create()
        self.ingredient2 = IngredientFactory.create()

        for codename in PERMS:
            perm = Permission.objects.get(codename=codename)
            self.user.user_permissions.add(perm)


class BasicUserProfileCase(SingleUserCase):
    """Basic test case for profile."""

    def test_user_has_profile(self):
        """Test that newly created User has ChefProfile."""
        self.assertTrue(self.user.profile)

    def test_profile_pk(self):
        """Test that newly created User's profile has a primary key."""
        self.assertIsInstance(self.user.profile.pk, int)
        self.assertTrue(self.user.profile.pk)

    def test_profile_is_active(self):
        """Test that profile of new User is active."""
        self.assertTrue(self.user.profile.is_active)

    def test_profile_active_manager(self):
        """Test that active attr is a Manager class."""
        self.assertIsInstance(ChefProfile.active, Manager)

    def test_profile_active_query(self):
        """Test that active manager can give a QuerySet."""
        self.assertIsInstance(ChefProfile.active.all(), QuerySet)

    def test_active_count(self):
        """Test that counting the active manager returns expected int."""
        self.assertEqual(ChefProfile.active.count(), 2)

    def test_about_me(self):
        """Test that User.profile.about_me can be added as expected."""
        self.assertEqual(self.user.profile.about_me, '')
        self.user.profile.about_me = 'Here is something about me'
        self.user.save()
        self.assertEqual(self.user.profile.about_me, 'Here is something about me')

    def test_favorites(self):
        """Ensure a user can have a favorite recipe."""
        self.assertNotIn(self.recipe, self.user.profile.favorites.all())
        self.user.profile.favorites.add(self.recipe)
        self.assertIn(self.recipe, self.user.profile.favorites.all())

    def test_liked_ingredient(self):
        """Test user can like a single ingredient."""
        self.user.profile.liked_ingredients.add(self.ingredient1)
        self.assertIn(self.ingredient1, self.user.profile.liked_ingredients.all())
        self.assertNotIn(self.ingredient2, self.user.profile.liked_ingredients.all())

    def test_disliked_ingredient(self):
        """Test that user can have disliked ingredients."""
        self.assertNotIn(self.ingredient2, self.user.profile.disliked_ingredients.all())
        self.user.profile.disliked_ingredients.add(self.ingredient2)
        self.assertIn(self.ingredient2, self.user.profile.disliked_ingredients.all())

    def test_has_add_ing_perm(self):
        """Test that user has permission to create an ingredient."""
        perms = [x.codename for x in self.user.user_permissions.all()]
        self.assertIn('add_ingredient', perms)

    def test_has_add_rec_perm(self):
        """Test that user has permission to create a recipe."""
        perms = [x.codename for x in self.user.user_permissions.all()]
        self.assertIn('add_recipe', perms)

    def test_has_add_rel_perm(self):
        """Test that user has permission to create a rec/ing/rel."""
        perms = [x.codename for x in self.user.user_permissions.all()]
        self.assertIn('add_recipeingredientrelationship', perms)

    def test_has__edit_perms(self):
        """Test that user has permission to edit an ingredient."""
        perms = [x.codename for x in self.user.user_permissions.all()]
        self.assertIn('change_ingredient', perms)

    def test_has__edit_rec_perms(self):
        """Test that user has permission to edit a recipe."""
        perms = [x.codename for x in self.user.user_permissions.all()]
        self.assertIn('change_recipe', perms)

    def test_edit_user(self):
        """Test that a user can edit their info."""
        perms = [x.codename for x in self.user.user_permissions.all()]
        self.assertIn('change_chefprofile', perms)
        self.assertIn('change_user', perms)

    def test_can_see_profile(self):
        """Test that profile view works."""
        client = Client()
        response = client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_non_logged_in_redirects(self):
        """Test that a non logged in user is redirected from edit."""
        client = Client()
        response = client.get('/profile/edit/')
        self.assertEqual(response.status_code, 302)

class ManyUsersCase(TestCase):
    """Test cases where many Users are registered."""

    def setUp(self):
        """Add many Users to the test."""
        self.user_batch = UserFactory.create_batch(USER_BATCH_SIZE)

    def test_active_count(self):
        """Make sure that the active user count is the expected size."""
        self.assertEqual(ChefProfile.active.count(), USER_BATCH_SIZE)



