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

    @patch('recipes.views.RECIPES_PER_PAGE', new=2)
    def test_recipe_homepage_pagination(self):
        # Make 10 recipes
        self.make_recipe_in_batch()

        # User opens browser
        self.browser.get(self.live_server_url)

        # user sees pagination and click on page 2
        page2 = self.browser.find_element(
            By.XPATH, '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )
        # If you want to see the magic
        # self.sleep(10)
