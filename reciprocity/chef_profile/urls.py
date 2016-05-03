"""Set URLs for profile specific views."""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import ProfileView, edit_profile

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='profile'),
    url(r'edit/$', login_required(edit_profile), name='edit_profile'),
]
