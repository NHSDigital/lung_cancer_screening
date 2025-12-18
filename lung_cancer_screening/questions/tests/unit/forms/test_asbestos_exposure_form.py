from django.test import TestCase

from ...factories.user_factory import UserFactory
from ....models.response_set import ResponseSet
from ....forms.asbestos_exposure_form import AsbestosExposureForm


class TestAsbestosExposureForm(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.response_set = ResponseSet(user=self.user)


    def test_is_valid_with_a_valid_value(self):
        form = AsbestosExposureForm(
            instance=self.response_set,
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
            instance=self.response_set,
            data={
                "user": self.user,
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
            instance=self.response_set,
            data={
                "user": self.user,
                "asbestos_exposure": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["asbestos_exposure"],
            ["Select if you have been exposed to asbestos"]
        )
