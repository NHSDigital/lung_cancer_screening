from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ....models.ethnicity_response import EthnicityResponse, EthnicityValues
from ....forms.ethnicity_form import EthnicityForm


class TestEthnicityForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.response = EthnicityResponse.objects.create(
            response_set=self.response_set,
            value=EthnicityValues.WHITE
        )

    def test_is_valid_with_a_valid_value(self):
        form = EthnicityForm(
            instance=self.response,
            data={
                'value': EthnicityValues.WHITE
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data['value'],
            EthnicityValues.WHITE
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = EthnicityForm(
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
        form = EthnicityForm(
            instance=self.response,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select your ethnic background"]
        )
