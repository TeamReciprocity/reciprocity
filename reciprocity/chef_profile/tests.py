"""Test ChefProfile model."""
from __future__ import unicode_literals
from django.conf import settings
from django.test import TestCase
from django.db.models import QuerySet, Manager
from .models import ChefProfile
import factory

USER_BATCH_SIZE = 20


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
        """Create a user for testing."""
        self.user = UserFactory.create()


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
        self.assertEqual(ChefProfile.active.count(), 1)


class ManyUsersCase(TestCase):
    """Test cases where many Users are registered."""

    def setUp(self):
        """Add many Users to the test."""
        self.user_batch = UserFactory.create_batch(USER_BATCH_SIZE)

    def test_active_count(self):
        """Make sure that the active user count is the expected size."""
        self.assertEqual(ChefProfile.active.count(), USER_BATCH_SIZE)

# test favorites:
# assert favorites is None
# create recipe, add to favorites
# assert recipe in favorites

# test likes/dislikes
# need ingredient factory
# test like favorites
