from django.shortcuts import render
from django.views.generic import TemplateView
from chef_profile.models import ChefProfile


class ProfileView(TemplateView):
    template_name = 'profile.html'
