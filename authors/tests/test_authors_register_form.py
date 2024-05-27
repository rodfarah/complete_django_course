from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('username', 'Your username'),
        ('email', 'Your e-mail address'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs.get('placeholder')
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('username',
         'Username length must be between 4 and 150 characters, '
         'with numbers, letters and @.+-_.'),
        ('email', 'The e-mail must be valid.'),
        ('password',
         'Password must have at least one uppercase letter,'
         'one lowercase letter and one number. The length should be '
         'at least 8 characters.'),
    ])
    def test_help_text_is_correct(self, field, needed):
        form = RegisterForm()
        current_help_text = form[field].field.help_text
        self.assertEqual(current_help_text, needed)

    @ parameterized.expand([
        ('first_name', "First Name"),
        ('last_name', "Last Name"),
        ('email', 'E-mail'),
        ('username', 'Username'),
        ('password', 'Password'),
        ('password2', 'Confirm Password')
    ])
    def test_fields_label_is_correct(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label
        self.assertEqual(current_label, label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'first_name': 'first',
            'last_name': 'last',
            'email': 'fulano@fulano.com',
            'username': 'user4',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1'
        }
        return super().setUp()

    @parameterized.expand([
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('username', 'Required. 4 to 150 characters or fewer. Letters, '
            'digits and @/./+/-/_ only.'),
        ('email', 'You must insert your e-mail address'),
        ('password', 'Password must not be empty'),
        ('password2', 'You must confirm your password'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_more_than_4_chars(self):
        self.form_data['username'] = 'hi'
        num_of_char = len(self.form_data['username'])
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Ensure this value has at least 4 characters'
        f'(it has {num_of_char}).'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_less_than_150_chars(self):
        self.form_data['username'] = 155*"a"
        num_of_char = len(self.form_data['username'])
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = ('Ensure this value has at most 150 characters '
               f'(it has {num_of_char}).')
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_numbers(self):
        self.form_data['password'] = 'abck23sdd'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = ('Password must have at least one uppercase letter'
               ', one lowercase letter and one number. '
               'The length should be at least 8 characters.')
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))

        self.form_data['password'] = 'Sbck23sdd'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_valid_password_doesnt_match_valid_password2(self):
        self.form_data['password'] = 'Adsd23*92'
        self.form_data['password2'] = 'YAdsd23*91'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Password and password2 must be equal'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(
            'password'))

    def test_register_view_raises_404_if_request_is_get(self):
        url = reverse('authors:create')
        response = self.client.get(url, data=self.form_data, follow=True)
        self.assertEqual(response.status_code, 404)

    def test_email_duplicity_raises_exception(self):
        url = reverse('authors:create')
        new_form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'fulano@fulano.com',
            'username': 'user3',
            'password': 'Str0ngP@ssword5',
            'password2': 'Str0ngP@ssword5'
        }

        self.client.post(url, data=new_form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'This username already exists. Choose a different one'
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    # Coverage demands this test, but I dont know how to code it

    # def test_register_create_messages_if_success(self):
    #     url = reverse('authors:create')
    #     response = self.client.post(url, data=self.form_data, follow=True)
    #     session_data = self.client.session['register_form_data']
    #     self.assertEqual(session_data['username'], 'user')
    #     messages = list(response.context['messages'])
    #     msg = 'You are now registered! Please, Log In'
    #     self.assertEqual(len(messages), 1)
    #     self.assertEqual(messages[0].message, msg)
    #     self.assertEqual(messages[0].level, constants.SUCCESS)
