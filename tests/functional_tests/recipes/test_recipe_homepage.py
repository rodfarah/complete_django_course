from selenium.webdriver.common.by import By
from .base import RecipeBaseFunctionalTest


class RecipeHomepageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_homepage_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here.', body.text)
