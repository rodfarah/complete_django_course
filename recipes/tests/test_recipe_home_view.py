from django.urls import reverse, resolve
from recipes import views
from unittest.mock import patch
from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):

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

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe(preparation_time=5, author_data={
            'first_name': 'Rodrigo'
        })
        response = self.client.get(reverse('recipes:home'))
        # content is the template html code. Check it out by using test debug with breakpoint. # noqa: 501
        content = response.content.decode('utf-8')
        # response.context['recipes'] is a queryset . Check it out by using test debug with breakpoint. # noqa: 501
        context = response.context['recipes']
        self.assertIn('Recipe Title', content)
        self.assertIn('5 Minutes', content)
        self.assertIn('Rodrigo', content)
        # check how many recipes were added
        self.assertEqual(len(context), 1)

    def test_recipe_home_template_doesnt_load_not_published_recipes(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertFalse(len(response.content) == 0)

    @patch('recipes.views.RECIPES_PER_PAGE', new=3)
    def test_recipe_home_is_paginated(self):
        self.make_recipe_in_batch(ammount=8)
        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator
        self.assertEqual(paginator.num_pages, 3)
        # Check if page one has 3 recipes
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(3)), 2)
