from django import forms
from utils.django_forms import add_placeholder


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        add_placeholder(
            field=self.fields['username'],
            placeholder_val='Type your username')
        add_placeholder(
            field=self.fields['password'],
            placeholder_val='Type your password')
