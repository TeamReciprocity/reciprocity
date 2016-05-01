from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

TIME_CHOICES = (
    (.25, '15 minutes'),
    (.5, '30 minutes'),
    (.75, '45 minutes'),
    (1, '1 hour'),
    (1.25, '1 hour 15 minutes'),
    (1.5, '1 hour 30 minutes'),
    (1.75, '1 hour 45 minutes'),
    (2, '2 hours'),
    (2.25, '2 hours 15 minutes'),
    (2.5, '2 hours 30 minutes'),
    (2.75, '2 hours 45 minutes'),
    (3, '3 hours'),
    (3.25, '3 hours 15 minutes'),
    (3.5, '3 hours 30 minutes'),
    (3.75, '3 hours 45 minutes'),
    (4, '4+ hours'),
)


@python_2_unicode_compatible
class Recipe(models.Model):
    """Instantiate a Recipe model instance."""

    def __str__(self):
        """Display model instance."""
        return self.recipe_name

    recipe_name = models.CharField(help_text='What is your recipe called?',
                                   max_length=128)
    prep_time = models.FloatField(choices=TIME_CHOICES,
                                  blank=True,
                                  null=True,)
    cook_time = models.FloatField(choices=TIME_CHOICES,
                                  blank=True,
                                  null=True,)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='authored_recipes')


