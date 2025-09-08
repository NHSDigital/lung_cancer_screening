from django.test import TestCase

from ....models.response_set import HaveYouEverSmokedValues
from ....forms.have_you_ever_smoked_form import HaveYouEverSmokedForm

class TestHaveYouEverSmokedForm(TestCase):
    def test_is_valid(self):
        form = HaveYouEverSmokedForm(
            data={"have_you_ever_smoked": HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY})
        self.assertTrue(form.is_valid())

    def test_is_invalid(self):
        form = HaveYouEverSmokedForm(data={"have_you_ever_smoked": "invalid"})
        self.assertFalse(form.is_valid())

    def test_returns_a_boolean_type(self):
        form = HaveYouEverSmokedForm(
            data={"have_you_ever_smoked": HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY})
        form.is_valid()
        self.assertEqual(
            form.cleaned_data["have_you_ever_smoked"], HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY.value)
