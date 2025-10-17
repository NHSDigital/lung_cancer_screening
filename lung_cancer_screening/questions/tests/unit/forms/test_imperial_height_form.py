from django.test import TestCase

from ....models.participant import Participant
from ....forms.imperial_height_form import ImperialHeightForm


class TestImperialHeightForm(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="1234567890")
        self.response_set = self.participant.responseset_set.create(
            height=1704
        )

    def test_is_valid_with_valid_input(self):
        form = ImperialHeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "height_imperial_0": "5",  # feet
                "height_imperial_1": "9"   # inches
            }
        )

        self.assertTrue(form.is_valid())

    def test_converts_feet_and_inches_to_an_inches_integer(self):
        form = ImperialHeightForm(
            participant=self.participant,
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
            participant=self.participant,
            data={
                "height_imperial_0": "5",  # feet
                "height_imperial_1": "9"   # inches
            }
        )
        form.save()
        self.assertEqual(self.response_set.height, None)

    def test_is_invalid_with_missing_data(self):
        form = ImperialHeightForm(
            participant=self.participant,
            instance=self.response_set,
            data={
                "height_imperial_0": "5",
                # missing inches
            }
        )
        self.assertFalse(form.is_valid())
