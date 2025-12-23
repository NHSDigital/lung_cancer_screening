from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ....models.weight_response import WeightResponse
from ....forms.metric_weight_form import MetricWeightForm


class TestMetricWeightForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.response = WeightResponse.objects.create(
            response_set=self.response_set,
            metric=700
        )

    def test_is_valid_with_valid_input(self):
        weight = "70.5"
        form = MetricWeightForm(
            instance=self.response,
            data={
                "metric": weight
            }
        )
        self.assertTrue(form.is_valid())

    def test_converts_kg_to_hundreds_of_grams_before_saving(self):
        weight = "70.5"
        form = MetricWeightForm(
            instance=self.response,
            data={
                "metric": weight
            }
        )

        form.is_valid()
        self.assertEqual(form.cleaned_data["metric"], 705)

    def test_converts_hundreds_of_grams_to_kg_before_rendering(self):
        self.response.metric = 705
        self.response.save()
        form = MetricWeightForm(
            instance=self.response
        )

        self.assertEqual(form["metric"].value(), 70.5)

    def test_is_not_valid_with_invalid_input(self):
        weight = "a"
        form = MetricWeightForm(
            instance=self.response,
            data={
                "metric": weight
            }
        )
        self.assertFalse(form.is_valid())

    # UAT: Error message when nothing is entered
    def test_error_message_when_weight_is_empty(self):
        form = MetricWeightForm(
            instance=self.response,
            data={
                "metric": ""
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["metric"], ["Enter your weight"])

    def test_is_not_valid_without_any_weight_value_set(self):
        form = MetricWeightForm(
            instance=self.response,
            data={
                "metric": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"metric": ["Enter your weight"]})

    # UAT: Error message for weight below minimum (25.4kg)
    def test_error_message_when_weight_below_minimum(self):
        form = MetricWeightForm(
            instance=self.response,
            data={
                "metric": "20.0"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Weight must be between 25.4kg and 317.5kg",
                    form.errors["metric"][0])

    # UAT: Error message for weight above maximum (317.5kg)
    def test_error_message_when_weight_above_maximum(self):
        form = MetricWeightForm(
            instance=self.response,
            data={
                "metric": "320.0"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Weight must be between 25.4kg and 317.5kg",
                    form.errors["metric"][0])

    # UAT: Edge case - minimum valid weight
    def test_accepts_minimum_valid_weight(self):
        form = MetricWeightForm(
            instance=self.response,
            data={
                "metric": "25.4"
            }
        )
        self.assertTrue(form.is_valid())

    # UAT: Edge case - maximum valid weight
    def test_accepts_maximum_valid_weight(self):
        form = MetricWeightForm(
            instance=self.response,
            data={
                "metric": "317.5"
            }
        )
        self.assertTrue(form.is_valid())

    def test_is_invalid_with_multiple_decimal_places(self):
        form = MetricWeightForm(
            instance=self.response,
            data={
                "metric": "100.01"  # too many decimal places
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["metric"],
            ["Kilograms must be to 1 decimal place, for example 90.2kgs"]
        )

    def test_setting_metric_weight_clears_imperial_weight(self):
        self.response.metric = None
        self.response.imperial = 66
        self.response.save()
        form = MetricWeightForm(
            instance=self.response,
            data={
                "metric": "70.5"
            }
        )
        form.save()
        self.response.refresh_from_db()
        self.assertEqual(self.response.imperial, None)
