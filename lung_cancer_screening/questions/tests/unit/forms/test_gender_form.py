from django.test import TestCase

from ....models.response_set import GenderValues
from ....models.participant import Participant
from ....forms.gender_form import GenderForm

class TestGenderForm(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="1234567890")

    def test_is_valid_with_a_valid_value(self):
        form = GenderForm(
            participant=self.participant,
            data={
                "gender": GenderValues.MALE
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["gender"],
            GenderValues.MALE.value
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = GenderForm(
            participant=self.participant,
            data={
                "gender": "invalid"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["gender"],
            ["Select a valid choice. invalid is not one of the available choices."]
        )

    def test_is_invalid_when_no_option_is_selected(self):
        form = GenderForm(
            participant=self.participant,
            data={
                "gender": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["gender"],
            ["Select the option that best describes your gender."]
        )
