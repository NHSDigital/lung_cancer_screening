from django.test import TestCase

from ...factories.user_factory import UserFactory
from ....models.response_set import ResponseSet
from ....forms.imperial_height_form import ImperialHeightForm


class TestImperialHeightForm(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.response_set = ResponseSet(user=self.user)
        self.response_set.height_metric = 1704

    def test_is_valid_with_valid_input(self):
        form = ImperialHeightForm(
            instance=self.response_set,
            data={
                "height_imperial_0": "5",  # feet
                "height_imperial_1": "9"   # inches
            }
        )

        self.assertTrue(form.is_valid())

    def test_converts_feet_and_inches_to_an_inches_integer(self):
        form = ImperialHeightForm(
            instance=self.response_set,
            data={
                "height_imperial_0": "5",  # feet
                "height_imperial_1": "9"   # inches
            }
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        self.assertEqual(form.cleaned_data['height_imperial'], 69)

    def test_setting_imperial_height_clears_height(self):
        form = ImperialHeightForm(
            instance=self.response_set,
            data={
                "height_imperial_0": "5",  # feet
                "height_imperial_1": "9"   # inches
            }
        )
        form.save()
        self.assertEqual(self.response_set.height_metric, None)

    def test_is_invalid_with_missing_data(self):
        form = ImperialHeightForm(
            instance=self.response_set,
            data={
                # missing feet
                # missing inches
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["height_imperial"],
            ["Enter your height"]
        )

    def test_is_invalid_with_missing_inches(self):
        form = ImperialHeightForm(
            instance=self.response_set,
            data={
                "height_imperial_0": "5",
                # missing inches
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["height_imperial"],
            ["Inches must be between 0 and 11"]
        )

    def test_is_invalid_with_missing_feet(self):
        form = ImperialHeightForm(
            instance=self.response_set,
            data={
                #"height_imperial_0": "5",
                "height_imperial_1": "5"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["height_imperial"],
            ["Feet must be between 4 and 8"]
        )

    def test_is_invalid_when_given_a_decimal_feet_value(self):
        form = ImperialHeightForm(
            instance=self.response_set,
            data={
                "height_imperial_0": "5.2",
                "height_imperial_1": "0"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["height_imperial"],
            ["Feet must be in whole numbers"]
        )

    def test_is_invalid_when_inches_under_11(self):
        form = ImperialHeightForm(
            instance=self.response_set,
            data={
                "height_imperial_0": "5",
                "height_imperial_1": "12"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["height_imperial"],
            ["Inches must be between 0 and 11"]
        )

    def test_is_invalid_when_inches_over_0(self):
        form = ImperialHeightForm(
            instance=self.response_set,
            data={
                "height_imperial_0": "5",
                "height_imperial_1": "-1"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["height_imperial"],
            ["Inches must be between 0 and 11"]
        )

    def test_is_invalid_when_feet_over_4(self):
        form = ImperialHeightForm(
            instance=self.response_set,
            data={
                "height_imperial_0": "3",
                "height_imperial_1": "10"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["height_imperial"],
            ["Feet must be between 4 and 8"]
        )

    def test_is_invalid_when_feet_under_8(self):
        form = ImperialHeightForm(
            instance=self.response_set,
            data={
                "height_imperial_0": "9",
                "height_imperial_1": "0"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["height_imperial"],
            ["Feet must be between 4 and 8"]
        )
