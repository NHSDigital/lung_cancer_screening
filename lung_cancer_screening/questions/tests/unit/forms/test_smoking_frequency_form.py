from django.test import TestCase, tag

from lung_cancer_screening.questions.forms.smoking_frequency_form import SmokingFrequencyForm
from lung_cancer_screening.questions.models.smoking_frequency_response import SmokingFrequencyValues
from lung_cancer_screening.questions.tests.factories.response_set_factory import ResponseSetFactory

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ....models.tobacco_smoking_history import TobaccoSmokingHistory, TobaccoSmokingHistoryTypes


@tag("SmokingFrequency")
class TestSmokingFrequencyForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory.create()
        self.normal_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            level=TobaccoSmokingHistory.Levels.NORMAL,
            complete=True
        )


    def test_is_valid_with_a_valid_value(self):
        form = SmokingFrequencyForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
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
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
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
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history,
            data={
                "value": 'some string'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Select a valid choice. some string is not one of the available choices.",
            form.errors["value"]
        )

    def test_shows_normal_label_for_normal_level(self):
        form = SmokingFrequencyForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=self.normal_smoking_history
        )
        self.assertEqual(form.fields["value"].label, "How often do you smoke cigarettes?")

    def test_shows_increased_label_for_increased_level(self):
        increased_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            level=TobaccoSmokingHistory.Levels.INCREASED,
        )
        form = SmokingFrequencyForm(
            response_set=self.response_set,
            tobacco_smoking_history_item=increased_smoking_history
        )
        self.assertEqual(form.fields["value"].label, f"When you smoked more than {self.get_normal_smoking_string()}, how often did you smoke cigarettes?")

    def get_normal_smoking_string(self):
        amount = self.normal_smoking_history.smoked_amount_response
        frequency = self.normal_smoking_history.smoking_frequency_response
        return f"{amount.value} {self.normal_smoking_history.human_type().lower()} a {frequency.get_value_display_as_singleton_text()}"
