from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

TIME_CHOICES = (
    (.25, '15 minutes'),
    (.5, '30 minutes'),
    (.75, '45 minutes'),
    (1.0, '1 hour'),
    (1.25, '1 hour 15 minutes'),
    (1.5, '1 hour 30 minutes'),
    (1.75, '1 hour 45 minutes'),
    (2.0, '2 hours'),
    (2.25, '2 hours 15 minutes'),
    (2.5, '2 hours 30 minutes'),
    (2.75, '2 hours 45 minutes'),
    (3.0, '3 hours'),
    (3.25, '3 hours 15 minutes'),
    (3.5, '3 hours 30 minutes'),
    (3.75, '3 hours 45 minutes'),
    (4.0, '4+ hours'),
)

PRIVACY_CHOICES = (
    ('pu', 'Public'),
    ('pr', 'Private'),
    # ('fr', 'Friends Only'),
)


@python_2_unicode_compatible
class Ingredient(models.Model):
    """Instantiate an Ingredient model instance."""

    def __str__(self):
        """Display model instance."""
        return self.name

    name = models.CharField(max_length=128)


@python_2_unicode_compatible
class Recipe(models.Model):
    """Instantiate a Recipe model instance."""

    def __str__(self):
        """Display model instance."""
        return self.title

    title = models.CharField(help_text='What is your recipe called?',
                             max_length=128)
    description = models.TextField(blank=True,
                                   null=True,
                                   help_text='Tell us about your recipe.')
    prep_time = models.FloatField(choices=TIME_CHOICES,
                                  blank=True,
                                  null=True,)
    cook_time = models.FloatField(choices=TIME_CHOICES,
                                  blank=True,
                                  null=True,)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='authored_recipes')
    privacy = models.CharField(max_length=2,
                               choices=PRIVACY_CHOICES,
                               default='pu')
    directions = models.TextField(help_text='How is this recipe prepared?')
    parent = models.ForeignKey('self',
                               related_name='variations',
                               null=True,
                               blank=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientRelationship'
    )
    created = models.DateTimeField(auto_now_add=True)


@python_2_unicode_compatible
class RecipeIngredientRelationship(models.Model):
    """Instantiate a Recipe, Ingredient relationship."""

    def __str__(self):
        """Display associated recipe and ingredient."""
        return 'Recipe: {}, Ingredient: {}'.format(self.recipe,
                                                   self.ingredient)

    recipe = models.ForeignKey(Recipe, related_name='ingredients_in_recipe')
    ingredient = models.ForeignKey(Ingredient)
    quantity = models.CharField(max_length=128)
