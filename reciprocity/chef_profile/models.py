from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from recipe.models import Recipe, Ingredient


class ActiveManager(models.Manager):
    """QuerySet of ChefProfiles attached to an active User."""

    def get_queryset(self):
        """Return QuerySet filtering only ChefProfiles with active users."""
        queryset = super(ActiveManager, self).get_queryset()
        return queryset.filter(user__is_active=True)


@python_2_unicode_compatible
class ChefProfile(models.Model):
    """Extend the Django user profile for reciprocity project."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='profile')
    favorites = models.ManyToManyField(Recipe,
                                       related_name='favorite_of',
                                       blank=True)
    liked_ingredients = models.ManyToManyField(Ingredient,
                                               related_name='liked_by',
                                               blank=True)
    disliked_ingredients = models.ManyToManyField(Ingredient,
                                                  related_name='disliked_by',
                                                  blank=True)
    about_me = models.TextField(null=True, blank=True, )

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        """String output for ChefProfile model."""
        return "Chef Profile for {}".format(self.user)

    def __repr__(self):
        """Representation of Chef Profile for command line."""
        name = '.'.join((__name__, self.__class__.__name__))
        return "{}(user={})".format(name, self.user)

    @property
    def is_active(self):
        """Return boolean of associated User's is_active boolean state."""
        return self.user.is_active
