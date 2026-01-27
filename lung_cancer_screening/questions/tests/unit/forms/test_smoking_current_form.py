from django.test import TestCase, tag

from ....models.tobacco_smoking_history import TobaccoSmokingHistoryTypes
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory

from ....models.smoking_current_response import SmokingCurrentResponse
from ....forms.smoking_current_form import SmokingCurrentForm


@tag("SmokingCurrent")
class TestSmokingCurrentForm(TestCase):
    def setUp(self):
        self.smoking_history = TobaccoSmokingHistoryFactory.create(
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )
        self.response = SmokingCurrentResponse.objects.create(
            tobacco_smoking_history=self.smoking_history,
            value=False
        )


    def test_is_valid_with_a_valid_value(self):
        form = SmokingCurrentForm(
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
        form = SmokingCurrentForm(
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
        form = SmokingCurrentForm(
            instance=self.response,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select if you currently smoke cigarettes"]
        )
