from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


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
          'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
         ('email', 'The e-mail must be valid.'),
         ('password',
          'Password must have at least one uppercase letter,'
          'one lowercase letter and one number. The length should be '
          'at least 8 characters.'),])
    def test_help_text_is_correct(self, field, help_text):
        form = RegisterForm()
        current_help_text = form[field].field.help_text
        self.assertEqual(current_help_text, help_text)

    @parameterized.expand(
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
