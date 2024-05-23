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
         'Required. 150 characters or fewer. Letters, '
         'digits and @/./+/-/_ only.'),
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
            'username': 'user',
            'password1': 'Str0ngP@ssword',
            'password2': 'Str0ngP@assword2'
        }
        return super().setUp()

    @parameterized.expand([
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('username', 'This field must not be empty'),
        ('email', 'You must insert your e-mail address'),
        ('password', 'Password must not be empty'),
        ('password2', 'You must confirm your password'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
