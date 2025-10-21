from django.test import TestCase

from ....models.participant import Participant
from ....forms.metric_weight_form import MetricWeightForm

class TestMetricWeightForm(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="1234567890")
        self.response_set = self.participant.responseset_set.create()

    def test_is_valid_with_valid_input(self):
        weight = "70.5"
        form = MetricWeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "weight_metric": weight
            }
        )
        self.assertTrue(form.is_valid())

    def test_is_not_valid_with_invalid_input(self):
        weight = "a"
        form = MetricWeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "weight_metric": weight
            }
        )
        self.assertFalse(form.is_valid())

    # UAT: Error message when nothing is entered
    def test_error_message_when_weight_is_empty(self):
        form = MetricWeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "weight_metric": ""
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["weight_metric"], ["Enter your weight."])

    def test_is_not_valid_without_any_weight_value_set(self):
        form = MetricWeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "weight_metric": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"weight_metric": ["Enter your weight."]})

    # UAT: Error message for weight below minimum (25.4kg)
    def test_error_message_when_weight_below_minimum(self):
        form = MetricWeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "weight_metric": "20.0"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Weight must be between 25.4kg and 317.5kg",
                    form.errors["weight_metric"][0])

    # UAT: Error message for weight above maximum (317.5kg)
    def test_error_message_when_weight_above_maximum(self):
        form = MetricWeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "weight_metric": "320.0"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("Weight must be between 25.4kg and 317.5kg",
                    form.errors["weight_metric"][0])

    # UAT: Edge case - minimum valid weight
    def test_accepts_minimum_valid_weight(self):
        form = MetricWeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "weight_metric": "25.4"
            }
        )
        self.assertTrue(form.is_valid())

    # UAT: Edge case - maximum valid weight
    def test_accepts_maximum_valid_weight(self):
        form = MetricWeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "weight_metric": "317.5"
            }
        )
        self.assertTrue(form.is_valid())
