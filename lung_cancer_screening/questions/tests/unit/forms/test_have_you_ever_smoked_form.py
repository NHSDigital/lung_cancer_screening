from django.test import TestCase

from ...factories.user_factory import UserFactory
from ....models.response_set import HaveYouEverSmokedValues
from ....forms.have_you_ever_smoked_form import HaveYouEverSmokedForm

class TestHaveYouEverSmokedForm(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_is_valid(self):
        form = HaveYouEverSmokedForm(
            user=self.user,
            data={
                "have_you_ever_smoked": HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY
            }
        )
        self.assertTrue(form.is_valid())

    def test_is_invalid(self):
        form = HaveYouEverSmokedForm(
            user=self.user,
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
            user=self.user,
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
            user=self.user,
            data={
                "have_you_ever_smoked": HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY
            }
        )
        form.is_valid()
        self.assertEqual(
            form.cleaned_data["have_you_ever_smoked"], HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY.value)
