from django.test import TestCase

from ....models.participant import Participant
from ....forms.metric_height_form import MetricHeightForm


class TestMetricHeightForm(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="1234567890")
        self.response_set = self.participant.responseset_set.create(
            height_imperial=68
        )

    def test_is_valid_with_valid_input(self):
        height = "170.4"
        form = MetricHeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "height": height
            }
        )
        self.assertTrue(form.is_valid())

    def test_converts_cm_to_mm(self):
        height = "170.4"
        form = MetricHeightForm(
            participant=self.participant,
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
            participant=self.participant,
            data={
                "height": height
            }
        )
        form.save()
        self.assertEqual(self.response_set.height_imperial, None)

    def test_is_invalid(self):
        form = MetricHeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "height": "invalid"
            }
        )
        self.assertFalse(form.is_valid())
