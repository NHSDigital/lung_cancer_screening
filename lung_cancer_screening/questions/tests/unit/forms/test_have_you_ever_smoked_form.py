from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ....models.have_you_ever_smoked_response import HaveYouEverSmokedResponse, HaveYouEverSmokedValues
from ....forms.have_you_ever_smoked_form import HaveYouEverSmokedForm


class TestHaveYouEverSmokedForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.response = HaveYouEverSmokedResponse.objects.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY
        )

    def test_is_valid(self):
        form = HaveYouEverSmokedForm(
            instance=self.response,
            data={
                "value": (
                    HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY
                )
            }
        )
        self.assertTrue(form.is_valid())

    def test_is_invalid(self):
        form = HaveYouEverSmokedForm(
            instance=self.response,
            data={
                "value": "invalid"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select a valid choice. invalid is not one of the available choices."]
        )

    def test_is_invalid_when_no_option_is_selected(self):
        form = HaveYouEverSmokedForm(
            instance=self.response,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select if you have ever smoked"]
        )

    def test_returns_a_boolean_type(self):
        form = HaveYouEverSmokedForm(
            instance=self.response,
            data={
                "value": (
                    HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY
                )
            }
        )
        form.is_valid()
        self.assertEqual(
            form.cleaned_data["value"],
            HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY.value
        )
