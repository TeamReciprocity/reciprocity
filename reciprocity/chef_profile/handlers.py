# -*- coding: utf-8 -*-
"""Handlers for pop-save and pre-delete events on User model."""
from __future__ import unicode_literals  # pragma: no cover
from django.conf import settings  # pragma: no cover
from django.db.models.signals import post_save, pre_delete  # pragma: no cover
from django.dispatch import receiver  # pragma: no cover
from .models import ChefProfile  # pragma: no cover
import logging  # pragma: no cover
from registration.signals import user_activated
from django.contrib.auth.models import Permission
from registration.backends.hmac.views import ActivationView


logger = logging.getLogger(__name__)  # pragma: no cover

MODELS = ['recipe', 'ingredient', 'recipeingredientrelationship']
ACTIONS = ['add', 'change', 'delete']
PERMS = ['_'.join((action, model)) for action in ACTIONS for model in MODELS]
PERMS += ['change_user', 'change_chefprofile']


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_imager_profile(sender, **kwargs):
    """Create and save an ChefProfile after every new User is created."""
    if kwargs.get('created', False):
        try:
            user = kwargs['instance']
            new_profile = ChefProfile(user=user)
            new_profile.save()
        except (KeyError, ValueError):
            logger.error('Unable to create ChefProfile for User instance.')


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def remove_chef_profile(sender, **kwargs):
    """Delete attached ChefProfile after User is deleted."""
    try:
        instance = kwargs['instance']
        instance.is_active = False
        instance.profile.delete()
        instance.save()
    except (KeyError, AttributeError):
        logger.warn('ChefProfile instance not deleted.')


@receiver(user_activated, sender=ActivationView)
def add_permissions(sender, **kwargs):
    """Give active users permissions to use site."""
    try:
        user = kwargs['user']
        try:
            for codename in PERMS:
                perm = Permission.objects.get(codename=codename)
                user.user_permissions.add(perm)
        except Permission.DoesNotExist:
            logger.error('Permission not found.')
    except (KeyError, ValueError):
        logger.error('User not sent with user_activated signal.')
