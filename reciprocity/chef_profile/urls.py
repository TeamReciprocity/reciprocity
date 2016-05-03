"""Set URLs for profile specific views."""
from django.conf.urls import url
from django.views.generic import TemplateView
from .views import ProfileView, edit_profile

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='profile'),
    url(r'edit/$', edit_profile, name='edit_profile')
]
