from django.test import TestCase, tag

from lung_cancer_screening.questions.forms.smoking_frequency_form import SmokingFrequencyForm
from lung_cancer_screening.questions.models.smoking_frequency_response import SmokingFrequencyValues

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.smoking_frequency_response_factory import SmokingFrequencyResponseFactory
from ....models.tobacco_smoking_history import TobaccoSmokingHistoryTypes


@tag("SmokingFrequency")
class TestSmokingFrequencyForm(TestCase):
    def setUp(self):
        self.smoking_history = TobaccoSmokingHistoryFactory.create(
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )
        self.response = SmokingFrequencyResponseFactory.build(
            tobacco_smoking_history=self.smoking_history
        )


    def test_is_valid_with_a_valid_value(self):
        form = SmokingFrequencyForm(
            instance=self.response,
            data={
                "value": SmokingFrequencyValues.DAILY.value
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            SmokingFrequencyValues.DAILY.value
        )

    def test_is_invalid_with_a_none_value(self):
        form = SmokingFrequencyForm(
            instance=self.response,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Select how often you smoke cigarettes",
            form.errors["value"]
        )


    def test_is_invalid_with_a_non_numeric_value(self):
        form = SmokingFrequencyForm(
            instance=self.response,
            data={
                "value": 'some string'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Select a valid choice. some string is not one of the available choices.",
            form.errors["value"]
        )
