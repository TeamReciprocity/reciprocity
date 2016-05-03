from django.views.generic import TemplateView
from recipe.models import Recipe


class HomeView(TemplateView):
    """Home page view showing latest recipes."""
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(HomeView, self).get_context_data(*args, **kwargs)
        context_data['latest_recipes'] = Recipe.objects.order_by('created')[:10]
        return context_data
