from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from chef_profile.models import ChefProfile
from .forms import UserForm, ChefProfileForm



class ProfileView(TemplateView):
    template_name = 'chef_profile/profile.html'


def edit_profile(request):
    """Allow user to edit their ImagerProfile, and limited fields of User."""
    user = request.user
    profile = request.user.profile
    user_form = UserForm(instance=user)
    profile_form = ChefProfileForm(instance=profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ChefProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/profile/')
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'chef_profile/edit_profile.html', context)
