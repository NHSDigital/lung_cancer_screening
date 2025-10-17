from django.test import TestCase

from ....models.participant import Participant
from ....forms.metric_height_form import MetricHeightForm


class TestMetricHeightForm(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="1234567890")

    def test_cm_to_mm(self):
        height = "170.4"
        form = MetricHeightForm(
            participant=self.participant,
            data={
                "height": height
            }
        )

        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data["height"], 1704)

    def test_is_invalid(self):
        form = MetricHeightForm(
            participant=self.participant,
            data={
                "height": "invalid"
            }
        )
        self.assertFalse(form.is_valid())
