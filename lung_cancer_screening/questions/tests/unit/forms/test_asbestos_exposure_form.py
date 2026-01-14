from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ....models.asbestos_exposure_response import AsbestosExposureResponse
from ....forms.asbestos_exposure_form import AsbestosExposureForm


@tag("AsbestosExposure")
class TestAsbestosExposureForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.response = AsbestosExposureResponse.objects.create(
            response_set=self.response_set,
            value=False
        )


    def test_is_valid_with_a_valid_value(self):
        form = AsbestosExposureForm(
            instance=self.response,
            data={
                "value": False
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            False
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = AsbestosExposureForm(
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
        form = AsbestosExposureForm(
            instance=self.response,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select if you have been exposed to asbestos"]
        )
