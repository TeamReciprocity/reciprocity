"""Set URLs for profile specific views."""
from django.conf.urls import url
from django.views.generic import TemplateView
from .views import ProfileView

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='profile',),
]
