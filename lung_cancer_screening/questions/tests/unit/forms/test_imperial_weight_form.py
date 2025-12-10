from django.test import TestCase

from ...factories.user_factory import UserFactory
from ....models.response_set import ResponseSet
from ....forms.imperial_weight_form import ImperialWeightForm


class TestImperialWeightForm(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.response_set = ResponseSet(user=self.user)
        self.response_set.weight_metric = 1704

    def test_is_valid_with_valid_input(self):
        form = ImperialWeightForm(
            instance=self.response_set,
            data={
                "weight_imperial_0": "5",  # stone
                "weight_imperial_1": "9"   # pounds
            }
        )

        self.assertTrue(form.is_valid())

    def test_converts_stone_and_pounds_to_kilograms_integer(self):
        form = ImperialWeightForm(
            instance=self.response_set,
            data={
                "weight_imperial_0": "5",  # stone
                "weight_imperial_1": "9"   # pounds
            }
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        self.assertEqual(form.cleaned_data['weight_imperial'], 79)

    def test_setting_weight_imperial_clears_weight_metric(self):
        form = ImperialWeightForm(
            instance=self.response_set,
            data={
                "weight_imperial_0": "5",  # stone
                "weight_imperial_1": "9"   # pounds
            }
        )
        form.save()
        self.assertEqual(self.response_set.weight_metric, None)

    def test_is_invalid_with_no_values_set(self):
        form = ImperialWeightForm(
            instance=self.response_set,
            data={}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["weight_imperial"],
            ["Enter your weight"]
        )


    def test_is_invalid_when_given_a_decimal_stone_value(self):
        form = ImperialWeightForm(
            instance=self.response_set,
            data={
                "weight_imperial_0": "5.2",
                "weight_imperial_1": "0"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["weight_imperial"],
            ["Stone must be in whole numbers"]
        )

    def test_is_invalid_with_missing_pounds(self):
        form = ImperialWeightForm(
            instance=self.response_set,
            data={
                "weight_imperial_0": "5",
                # missing pounds
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["weight_imperial"],
            ["Pounds must be between 0 and 13"]
        )

    def test_is_invalid_with_missing_stone(self):
        form = ImperialWeightForm(
            instance=self.response_set,
            data={
                # missing stone
                "weight_imperial_1": "5"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["weight_imperial"],
            ["Stone must be between 4 and 50"]
        )

    def test_is_invalid_when_pounds_under_0(self):
        form = ImperialWeightForm(
            instance=self.response_set,
            data={
                "weight_imperial_0": "5",
                "weight_imperial_1": "-1"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["weight_imperial"],
            ["Pounds must be between 0 and 13"]
        )

    def test_is_invalid_when_pounds_over_13(self):
        form = ImperialWeightForm(
            instance=self.response_set,
            data={
                "weight_imperial_0": "5",
                "weight_imperial_1": "14"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["weight_imperial"],
            ["Pounds must be between 0 and 13"]
        )

    def test_is_invalid_when_stone_under_4(self):
        form = ImperialWeightForm(
            instance=self.response_set,
            data={
                "weight_imperial_0": "3",
                "weight_imperial_1": "10"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["weight_imperial"],
            ["Weight must be between 4 stone and 50 stone"]
        )

    def test_is_invalid_when_stone_over_50(self):
        form = ImperialWeightForm(
            instance=self.response_set,
            data={
                "weight_imperial_0": "51",
                "weight_imperial_1": "0"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["weight_imperial"],
            ["Weight must be between 4 stone and 50 stone"]
        )
