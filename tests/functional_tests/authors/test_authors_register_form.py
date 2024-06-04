from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AuthorsRegisterTest(AuthorsBaseTest):

    def get_by_placeholder(self, web_element: str, placeholder_text: str):
        field = web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder_text}"]')
        return field

    def get_form(self):
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
        )
        return form

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + "/authors/register/")
        form = self.get_form()
        self.fill_form_dummy_data(form=form)
        form.find_element(
            By.NAME,
            'email'
        ).send_keys('dummy@email.com')
        callback(form)
        return form

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, "input")
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, "First Name")
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn("Write your first name", form.text)
        self.form_field_test_with_callback(callback=callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, "Last Name")
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn("Write your last name", form.text)
        self.form_field_test_with_callback(callback=callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, "Your username")
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn(
                'Required. 4 to 150 characters or fewer. Letters, '
                'digits and @/./+/-/_ only.',
                form.text)
        self.form_field_test_with_callback(callback=callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, "Your e-mail address")
            # Delete string from field
            for n in range(len(email_field.get_attribute("value"))):
                email_field.send_keys(Keys.LEFT)
                email_field.send_keys(Keys.DELETE)
            email_field.send_keys("test@test")
            self.sleep(8)
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn(
                'Enter a valid email address.',
                form.text)
        self.form_field_test_with_callback(callback=callback)

    def test_different_passwords_error_message(self):
        def callback(form):
            password2_field = self.get_by_placeholder(
                form, "Repeat your password")
            password2_field.send_keys('a'*10)
            password2_field.send_keys(Keys.ENTER)
            self.sleep(2)
            form = self.get_form()
            pwd2_error_msg = form.find_element(
                By.XPATH,
                '/html/body/main/div[2]/form/div[1]/div[6]/ul/li')
            expected_message = 'Password and password2 must be equal'
            self.assertEqual(expected_message, pwd2_error_msg.text)
        self.form_field_test_with_callback(callback=callback)

    def test_user_valid_data_register_successfuly(self):
        self.browser.get(self.live_server_url + "/authors/register/")
        form = self.get_form()
        self.get_by_placeholder(form, 'First Name').send_keys('My')
        self.get_by_placeholder(form, 'Last Name').send_keys('Name')
        self.get_by_placeholder(
            form, 'Your username').send_keys('my_username')
        self.get_by_placeholder(
            form, 'Your e-mail address').send_keys('email@email.com')
        self.get_by_placeholder(form, 'Your password').send_keys('P@ssw0rd')
        self.get_by_placeholder(
            form, 'Repeat your password').send_keys('P@ssw0rd')
        form.submit()
        expected_message = 'You are now registered! Please, Log In'
        self.assertIn(expected_message, self.browser.find_element(
            By.CLASS_NAME, 'message-success').text)
