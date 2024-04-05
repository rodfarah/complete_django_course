from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_model_fields_max_lenght(self, field_name, max_lenght):
        setattr(self.recipe, field_name, "A" * (max_lenght + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
