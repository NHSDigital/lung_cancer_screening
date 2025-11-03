from django.test import TestCase

from ....models.response_set import EthnicityValues
from ....models.participant import Participant
from ....forms.ethnicity_form import EthnicityForm

class TestEthnicityForm(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="1234567890")

    def test_is_valid_with_a_valid_value(self):
        form = EthnicityForm(
            participant=self.participant,
            data={
                'ethnicity': EthnicityValues.WHITE
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
          form.cleaned_data['ethnicity'],
          EthnicityValues.WHITE
        )
    
    def test_is_invalid_with_an_invalid_value(self):
        form = EthnicityForm(
            participant=self.participant,
            data={
                "ethnicity": "invalid"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["ethnicity"],
            ["Select a valid choice. invalid is not one of the available choices."]
        )

    def test_is_invalid_when_no_option_is_selected(self):
        form = EthnicityForm(
            participant=self.participant,
            data={
                "ethnicity": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["ethnicity"],
            ["Select your ethnic background."]
        )