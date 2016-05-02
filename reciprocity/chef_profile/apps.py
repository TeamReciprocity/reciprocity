from django.apps import AppConfig


class ChefProfileConfig(AppConfig):
    """Set up config to ChefProfile."""
    name = 'chef_profile'

    def ready(self):
        """Run code when the app is ready."""
        from chef_profile import handlers

