from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_correct_recipe(self):
        needed_title = 'This is a detail page - It loads one recipe'
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse(
            'recipes:recipe',
            kwargs={'id': 1}
        ))
        # content is the template html code. Check it out by using test debug with breakpoint.
        content = response.content.decode('utf-8')
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_doesnt_load_not_published_recipes(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id}))
        self.assertFalse(len(response.content) == 0)
