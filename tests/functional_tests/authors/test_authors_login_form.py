import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest

# from selenium.webdriver.common.keys import Keys


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

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url +
                         reverse('authors:login_create'))
        self.assertIn('Not Found', self.browser.find_element(
            By.TAG_NAME, 'h1').text
        )

    def test_login_invalid_form_raises_error_message(self):
        # User opens login page
        self.browser.get(self.live_server_url +
                         reverse('authors:login'))
        # we now get the form and find username field
        form = self.get_login_form()
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # user inserts only one space as username (Django kills empty spaces)
        username_field.send_keys(' ')
        password_field.send_keys(' ')
        # user sends form
        form.submit()

        self.assertIn(
            'Form data is not valid.',
            self.browser.find_element(By.CLASS_NAME, 'message-error').text
        )

    def test_login_form_invalid_credentials(self):
        # User opens login page
        self.browser.get(self.live_server_url +
                         reverse('authors:login'))
        # we now get the form and find username field
        form = self.get_login_form()
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # user inserts unmatched username and password
        username_field.send_keys('invalid_username')
        password_field.send_keys('invalid_password')
        # user sends form
        form.submit()

        self.assertIn(
            'Invalid username and/or password. Please, try again.',
            self.browser.find_element(By.CLASS_NAME, 'message-error').text
        )
