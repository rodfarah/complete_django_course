import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest.mock import patch
from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomepageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_homepage_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here.', body.text)

    @patch('recipes.views.RECIPES_PER_PAGE', new=2)
    def test_recipe_search_input_finds_correct_recipes(self):
        # Make 10 recipes
        recipes = self.make_recipe_in_batch()
        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()
        # open browser
        self.browser.get(self.live_server_url)
        # find search field whith placeholder
        searchfield = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Search for a recipe..."]'
        )
        # Click search field and insert search text
        searchfield.send_keys(title_needed)
        # search field enter
        searchfield.send_keys(Keys.ENTER)
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )
