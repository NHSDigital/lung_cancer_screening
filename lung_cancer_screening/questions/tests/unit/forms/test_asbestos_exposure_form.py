from django.test import TestCase

from ...factories.user_factory import UserFactory
from ....forms.asbestos_exposure_form import AsbestosExposureForm


class TestAsbestosExposureForm(TestCase):
    def setUp(self):
        self.user = UserFactory()


    def test_is_valid_with_a_valid_value(self):
        form = AsbestosExposureForm(
            user=self.user,
            data={
                "asbestos_exposure": False
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["asbestos_exposure"],
            False
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = AsbestosExposureForm(
            user=self.user,
            data={
                "asbestos_exposure": "invalid"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["asbestos_exposure"],
            ["Select a valid choice. invalid is not one of the available choices."]
        )

    def test_is_invalid_when_no_option_is_selected(self):
        form = AsbestosExposureForm(
            user=self.user,
            data={
                "asbestos_exposure": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["asbestos_exposure"],
            ["Select if you have been exposed to asbestos"]
        )
