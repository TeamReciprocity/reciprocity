from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from reciprocity.models import Recipe


@python_2_unicode_compatible
class ChefProfile(models.Manager):
    """Extend the Django user profile for reciprocity project."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    favorites = models.ManyToManyField(Recipe, related_name='favorite_of')

    objects = models.Manager()

    def __str__(self):
        """String output for ChefProfile model."""
        return "Chef Profile for {}".format(self.user)

    def __repr__(self):
        """Representation of Chef Profile for command line."""
        name = '.'.join((__name__, self.__class__.__name__))
        return "{}(user={})".format(name, self.user)
