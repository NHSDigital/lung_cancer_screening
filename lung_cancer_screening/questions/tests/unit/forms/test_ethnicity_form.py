from django.test import TestCase

from ...factories.user_factory import UserFactory
from ....models.response_set import EthnicityValues
from ....forms.ethnicity_form import EthnicityForm

class TestEthnicityForm(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_is_valid_with_a_valid_value(self):
        form = EthnicityForm(
            user=self.user,
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
            user=self.user,
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
            user=self.user,
            data={
                "ethnicity": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["ethnicity"],
            ["Select your ethnic background"]
        )
