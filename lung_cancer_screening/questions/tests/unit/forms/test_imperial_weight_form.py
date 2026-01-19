from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ....models.weight_response import WeightResponse
from ....forms.imperial_weight_form import ImperialWeightForm


@tag("Weight")
class TestImperialWeightForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.response = WeightResponse.objects.create(
            response_set=self.response_set,
            metric=1704
        )

    def test_is_valid_with_valid_input(self):
        form = ImperialWeightForm(
            instance=self.response,
            data={
                "imperial_0": "5",  # stone
                "imperial_1": "9"   # pounds
            }
        )

        self.assertTrue(form.is_valid())

    def test_converts_stone_and_pounds_to_kilograms_integer(self):
        form = ImperialWeightForm(
            instance=self.response,
            data={
                "imperial_0": "5",  # stone
                "imperial_1": "9"   # pounds
            }
        )

        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        self.assertEqual(form.cleaned_data['imperial'], 79)

    def test_setting_weight_imperial_clears_weight_metric(self):
        form = ImperialWeightForm(
            instance=self.response,
            data={
                "imperial_0": "5",  # stone
                "imperial_1": "9"   # pounds
            }
        )
        form.save()
        self.response.refresh_from_db()
        self.assertEqual(self.response.metric, None)

    def test_is_invalid_with_no_values_set(self):
        form = ImperialWeightForm(
            instance=self.response,
            data={}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["imperial"],
            ["Enter your weight"]
        )


    def test_is_invalid_when_given_a_decimal_stone_value(self):
        form = ImperialWeightForm(
            instance=self.response,
            data={
                "imperial_0": "5.2",
                "imperial_1": "0"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["imperial"],
            ["Stone must be in whole numbers"]
        )

    def test_is_invalid_with_missing_pounds(self):
        form = ImperialWeightForm(
            instance=self.response,
            data={
                "imperial_0": "5",
                # missing pounds
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["imperial"],
            ["Pounds must be between 0 and 13"]
        )

    def test_is_invalid_with_missing_stone(self):
        form = ImperialWeightForm(
            instance=self.response,
            data={
                # missing stone
                "imperial_1": "5"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["imperial"],
            ["Stone must be between 4 and 50"]
        )

    def test_is_invalid_when_pounds_under_0(self):
        form = ImperialWeightForm(
            instance=self.response,
            data={
                "imperial_0": "5",
                "imperial_1": "-1"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["imperial"],
            ["Pounds must be between 0 and 13"]
        )

    def test_is_invalid_when_pounds_over_13(self):
        form = ImperialWeightForm(
            instance=self.response,
            data={
                "imperial_0": "5",
                "imperial_1": "14"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["imperial"],
            ["Pounds must be between 0 and 13"]
        )

    def test_is_invalid_when_stone_under_4(self):
        form = ImperialWeightForm(
            instance=self.response,
            data={
                "imperial_0": "3",
                "imperial_1": "10"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["imperial"],
            ["Weight must be between 4 stone and 50 stone"]
        )

    def test_is_invalid_when_stone_over_50(self):
        form = ImperialWeightForm(
            instance=self.response,
            data={
                "imperial_0": "51",
                "imperial_1": "0"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["imperial"],
            ["Weight must be between 4 stone and 50 stone"]
        )

    def test_setting_imperial_weight_clears_metric_weight(self):
        self.response.metric = 705
        self.response.save()
        form = ImperialWeightForm(
            instance=self.response,
            data={
                "imperial_0": "5",
                "imperial_1": "9"
            }
        )
        form.save()
        self.response.refresh_from_db()
        self.assertEqual(self.response.metric, None)
