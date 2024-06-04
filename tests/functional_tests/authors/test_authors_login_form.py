import pytest
from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from django.urls import reverse


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):

    def get_login_form(self):
        login_form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )
        return login_form

    def test_user_valid_data_can_login_successfully(self):
        # create user
        User.objects.create_user(
            username='my_user', password='P@ssw0rd')
        # open browser and get form as a web element
        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.get_login_form()
        # get username and password fields
        username_field = self.get_by_placeholder(
            web_element=form,
            placeholder_text='Type your username'
        )
        password_field = self.get_by_placeholder(
            web_element=form,
            placeholder_text='Type your password'
        )
        # insert username and password in its fields
        username_field.send_keys('my_user')
        password_field.send_keys('P@ssw0rd')
        # submit form
        form.submit()
        # assertion
        expected_message = 'You are now logged in as my_user!'
        self.assertIn(
            expected_message,
            self.browser.find_element(By.CLASS_NAME, 'message-success').text
        )
