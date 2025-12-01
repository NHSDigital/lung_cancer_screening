from django.test import TestCase

from ....models.response_set import HaveYouEverSmokedValues
from ....models.participant import Participant
from ....forms.have_you_ever_smoked_form import HaveYouEverSmokedForm

class TestHaveYouEverSmokedForm(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="1234567890")

    def test_is_valid(self):
        form = HaveYouEverSmokedForm(
            participant=self.participant,
            data={
                "have_you_ever_smoked": HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY
            }
        )
        self.assertTrue(form.is_valid())

    def test_is_invalid(self):
        form = HaveYouEverSmokedForm(
            participant=self.participant,
            data={
                "have_you_ever_smoked": "invalid"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["have_you_ever_smoked"],
            ["Select a valid choice. invalid is not one of the available choices."]
        )

    def test_is_invalid_when_no_option_is_selected(self):
        form = HaveYouEverSmokedForm(
            participant=self.participant,
            data={
                "have_you_ever_smoked": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["have_you_ever_smoked"],
            ["Select if you have ever smoked"]
        )

    def test_returns_a_boolean_type(self):
        form = HaveYouEverSmokedForm(
            participant=self.participant,
            data={
                "have_you_ever_smoked": HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY
            }
        )
        form.is_valid()
        self.assertEqual(
            form.cleaned_data["have_you_ever_smoked"], HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY.value)
