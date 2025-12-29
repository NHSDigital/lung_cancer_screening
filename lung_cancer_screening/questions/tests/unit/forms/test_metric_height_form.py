from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ....models.height_response import HeightResponse
from ....forms.metric_height_form import MetricHeightForm


class TestMetricHeightForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.response = HeightResponse.objects.create(
            response_set=self.response_set,
            imperial=68
        )

    def test_is_valid_with_valid_input(self):
        height_metric = "170.4"
        form = MetricHeightForm(
            instance=self.response,
            data={
                "metric": height_metric
            }
        )
        self.assertTrue(form.is_valid())

    def test_converts_cm_to_mm_before_saving(self):
        height_metric = "170.4"
        form = MetricHeightForm(
            instance=self.response,
            data={
                "metric": height_metric
            }
        )

        form.is_valid()
        self.assertEqual(form.cleaned_data["metric"], 1704)

    def test_converts_mm_to_cm_before_rendering(self):
        self.response.imperial = None
        self.response.metric = 1704
        self.response.save()
        form = MetricHeightForm(
            instance=self.response
        )

        self.assertEqual(form["metric"].value(), 170.4)


    def test_setting_height_clears_imperial_height(self):
        height_metric = "170.4"
        form = MetricHeightForm(
            instance=self.response,
            data={
                "metric": height_metric
            }
        )
        form.save()
        self.response.refresh_from_db()
        self.assertEqual(self.response.imperial, None)

    def test_is_invalid(self):
        form = MetricHeightForm(
            instance=self.response,
            data={
                "metric": "invalid"
            }
        )
        self.assertFalse(form.is_valid())

    def test_is_invalid_with_multiple_decimal_places(self):
        form = MetricHeightForm(
            instance=self.response,
            data={
                "metric": "170.45"  # too many decimal places
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["metric"],
            ["Centimetres must be to 1 decimal place, for example 185.5cm"]
        )
