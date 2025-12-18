from django.test import TestCase

from ...factories.user_factory import UserFactory
from ....models.response_set import ResponseSet, EthnicityValues
from ....forms.ethnicity_form import EthnicityForm


class TestEthnicityForm(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.response_set = ResponseSet(user=self.user)

    def test_is_valid_with_a_valid_value(self):
        form = EthnicityForm(
            instance=self.response_set,
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
            instance=self.response_set,
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
            instance=self.response_set,
            data={
                "ethnicity": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["ethnicity"],
            ["Select your ethnic background"]
        )
