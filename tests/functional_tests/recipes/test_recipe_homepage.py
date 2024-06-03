import pytest
from selenium.webdriver.common.by import By
from unittest.mock import patch
from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomepageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.RECIPES_PER_PAGE', new=2)
    def test_recipe_homepage_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here.', body.text)
