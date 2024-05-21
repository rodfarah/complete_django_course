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
        ('email', 'Your e-mail'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand(
        [('username',
          'Required. 150 characters or fewer. Letters, '
          'digits and @/./+/-/_ only.'),
         ('email', 'The e-mail must be valid.'),
         ('password',
          'Password must have at least one uppercase letter,'
          'one lowercase letter and one number. The length should be '
          'at least 8 characters.'),])
    def test_help_text_is_correct(self, field, help_text):
        form = RegisterForm()
        current_help_text = form[field].field.help_text
        self.assertEqual(current_help_text, help_text)

    @ parameterized.expand(
        [('username', 'Username'),
         ('email', 'E-mail'),
         ('password', 'Password'),
         ('first_name', "First name"),
         ('last_name', "Last name"),
         ('password2', 'Confirm Password')
         ])
    def test_fields_label_is_correct(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label
        self.assertEqual(current_label, label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': '',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'fulano@fulano.com',
            'password1': 'Str0ngP@ssword',
            'password2': 'Str0ngP@assword2'
        }
        return super().setUp()

    @parameterized.expand(
        [('username', 'This field must not be empty'),]
    )
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
