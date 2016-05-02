# -*- coding: utf-8 -*-
"""Handlers for pop-save and pre-delete events on User model."""
from __future__ import unicode_literals
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import ChefProfile
import logging

logger = logging.getLogger(__name__)


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
