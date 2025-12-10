from django.test import TestCase

from ...factories.user_factory import UserFactory
from ....models.response_set import ResponseSet
from ....forms.metric_height_form import MetricHeightForm


class TestMetricHeightForm(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.response_set = ResponseSet(user=self.user)
        self.response_set.height_imperial = 68

    def test_is_valid_with_valid_input(self):
        height = "170.4"
        form = MetricHeightForm(
            instance=self.response_set,
            data={
                "height": height
            }
        )
        self.assertTrue(form.is_valid())

    def test_converts_cm_to_mm(self):
        height = "170.4"
        form = MetricHeightForm(
            instance=self.response_set,
            data={
                "height": height
            }
        )

        form.is_valid()
        self.assertEqual(form.cleaned_data["height"], 1704)

    def test_setting_height_clears_imperial_height(self):
        height = "170.4"
        form = MetricHeightForm(
            instance=self.response_set,
            data={
                "height": height
            }
        )
        form.save()
        self.assertEqual(self.response_set.height_imperial, None)

    def test_is_invalid(self):
        form = MetricHeightForm(
            instance=self.response_set,
            data={
                "height": "invalid"
            }
        )
        self.assertFalse(form.is_valid())

    def test_is_invalid_with_multiple_decimal_places(self):
        form = MetricHeightForm(
            instance=self.response_set,
            data={
                "height": "170.45"  # too many decimal places
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["height"],
            ["Centimetres must be to 1 decimal place, for example 185.5cm"]
        )
