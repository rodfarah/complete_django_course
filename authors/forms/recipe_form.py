from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_negative_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create a dict in order to check all errors (in one strike) in form,
        # instead of each one
        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'preparation_time',
                  'preparation_time_unit', 'servings', 'servings_unit',
                  'preparation_steps', 'cover']
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Portions', 'Portions'),
                    ('Slices', 'Slices'),
                    ('Cups', 'Cups'),
                    ('Plates', 'Plates'),
                    ('Glasses', 'Glasses'),
                    ('Pieces', 'Pieces'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutes', 'Minutes'),
                    ('Hours', 'Hours'),
                    ('Seconds', 'Seconds'),
                )
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title == description:
            self._my_errors['description'].append(
                'Description can not be equal to title')

        if self._my_errors:
            raise ValidationError(self._my_errors)
        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append('Must have at least 5 characters')

        return title

    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')

        if is_negative_number(preparation_time):
            self._my_errors['preparation_time'].append(
                'Must be a positive number')

        return preparation_time

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')

        if is_negative_number(servings):
            self._my_errors['servings'].append(
                'Must be a positive number')

        return servings
