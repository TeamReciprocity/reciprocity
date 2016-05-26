from django.test import Client, TestCase
from recipe.tests import RecipeFactory, UserFactory


class ViewHome(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.public_recipe = RecipeFactory(author=self.user, privacy='pu')
        self.private_recipe = RecipeFactory(author=self.user, privacy='pr')

    def test_including(self):
        """Confirm view lists user's recipes."""
        response = self.client.get('/')
        self.assertIn(str(self.public_recipe), str(response.content))

    def test_excluding(self):
        """Confirm view excludes non-authored recipes."""
        response = self.client.get('/')
        self.assertNotIn(str(self.private_recipe), str(response.content))
