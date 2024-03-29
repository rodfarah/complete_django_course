from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(
            response=response, template_name='recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found here.',
                      response.content.decode('utf-8'))

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_onerecipe_view_function_is_correct(self):
        view = resolve(reverse('recipes:one_recipe', kwargs={'one_id': 1}))
        self.assertIs(view.func, views.one_recipe)

    def test_recipe_onerecipe_returns_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse(
                'recipes:one_recipe',
                kwargs={'one_id': 1000}))
        self.assertEqual(response.status_code, 404)
