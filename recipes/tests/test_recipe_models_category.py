from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class CategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Test'
        )
        return super().setUp()

    def test_recipe_category_model_str_repr_equals_name(self):
        self.category.name = 'Testing Category Name'
        self.category.full_clean()
        self.category.save()
        self.assertEqual(str(self.category), 'Testing Category Name')

    def test_recipe_category_model_name_max_length_65_chars(self):
        self.category.name = "a" * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
