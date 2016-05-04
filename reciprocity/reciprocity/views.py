from django.views.generic import TemplateView
from recipe.models import Recipe


class HomeView(TemplateView):
    """Home page view showing latest recipes."""
    template_name = 'reciprocity/home.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(HomeView, self).get_context_data(*args, **kwargs)
        queryset = Recipe.objects.filter(privacy='pu')
        context_data['latest_recipes'] = queryset.order_by('-created')[:10]
        return context_data
