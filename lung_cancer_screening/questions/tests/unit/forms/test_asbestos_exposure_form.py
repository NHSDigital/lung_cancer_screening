from django.test import TestCase

from ....models.response_set import AsbestosExposureValues
from ....models.participant import Participant
from ....forms.asbestos_exposure_form import AsbestosExposureForm


class TestAsbestosExposureForm(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="1234567890")

    def test_is_valid_with_yes(self):
        form = AsbestosExposureForm(
            participant=self.participant,
            data={
                "asbestos_exposure": AsbestosExposureValues.YES
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["asbestos_exposure"],
            AsbestosExposureValues.YES.value
        )

    def test_is_valid_with_no(self):
        form = AsbestosExposureForm(
            participant=self.participant,
            data={
                "asbestos_exposure": AsbestosExposureValues.NO
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["asbestos_exposure"],
            AsbestosExposureValues.NO.value
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = AsbestosExposureForm(
            participant=self.participant,
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
            participant=self.participant,
            data={
                "asbestos_exposure": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["asbestos_exposure"],
            ["Select if you have been exposed to asbestos."]
        )
