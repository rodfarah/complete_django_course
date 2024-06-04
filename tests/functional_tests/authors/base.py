from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
import time
from selenium.webdriver.common.by import By


class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, ammount=10):
        time.sleep(ammount)

    def get_by_placeholder(self, web_element: str, placeholder_text: str):
        field = web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder_text}"]')
        return field
