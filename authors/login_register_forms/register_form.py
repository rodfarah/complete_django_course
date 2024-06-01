from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, add_attr, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail address')
        add_placeholder(self.fields['first_name'], 'First Name')
        add_placeholder(self.fields['last_name'], 'Last Name')
        # as an example, it is even possible to add a css class to the html
        add_attr(self.fields['username'], 'css', 'a-css-class')

    username = forms.CharField(
        label="Username",
        help_text="Username length must be between 4 and 150 characters, "
        "with numbers, letters and @.+-_.",
        min_length=4,
        max_length=150,
        error_messages={
            'required': 'Required. 4 to 150 characters or fewer. Letters, '
            'digits and @/./+/-/_ only.',
        }
    )

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        # required = True is already a default so we may ommit it
        # required=True,
        label='First Name'
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        # required=True,
        label='Last Name'
    )
    email = forms.EmailField(
        # required=True,
        # widget=forms.EmailInput(attrs={
        #     'placeholder': 'Insert your e-mail address'
        # }),
        error_messages={
            'required': 'You must insert your e-mail address'
        },
        help_text='The e-mail must be valid.',
        label='E-mail',
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'

        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter,'
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password],
        label="Password"

    )
    password2 = forms.CharField(
        # required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        }),
        error_messages={
            'required': 'You must confirm your password'
        },
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):

        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'This username already exists. Choose a different one',
                code='invalid'
            )
        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password2 must be equal',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
