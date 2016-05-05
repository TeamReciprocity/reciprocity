from django import forms
from chef_profile.models import ChefProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    """Modifying limited fields on the User model."""

    class Meta:
        """Establish Model and fields for user form."""

        model = User
        fields = ['first_name', 'last_name', 'email']


class ChefProfileForm(forms.ModelForm):
    """Editable Profile for the user."""

    class Meta:
        """Establish Model and fields for user form."""

        model = ChefProfile
        exclude = ['user', 'favorites', 'disliked_ingredients', 'liked_ingredients']
