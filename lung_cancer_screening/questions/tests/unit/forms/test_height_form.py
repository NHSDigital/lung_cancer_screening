from django.test import TestCase

from ....models.participant import Participant
from ....forms.height_form import HeightForm

class TestHeightForm(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="1234567890")

    def test_cm_to_mm(self):
        height = "170.4"
        form = HeightForm(
            participant=self.participant,
            data={
                "height_in_cm": height
            }
        )
        
        self.assertTrue(form.is_valid())
        
        self.assertEqual(form.cleaned_data["height_in_cm"], 1704)

    def test_is_invalid(self):
        form = HeightForm(
            participant=self.participant,
            data={
                "height_in_cm": "invalid"
            }
        )
        self.assertFalse(form.is_valid())
