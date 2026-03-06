from django.test import TestCase, tag

from lung_cancer_screening.questions.forms.smoking_frequency_form import SmokingFrequencyForm
from lung_cancer_screening.questions.models.smoking_frequency_response import SmokingFrequencyValues
from lung_cancer_screening.questions.tests.factories.response_set_factory import ResponseSetFactory

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory


@tag("SmokingFrequency", "wip")
class TestSmokingFrequencyForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory.create(complete=True)
        self.normal_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            normal=True,
            pipe=True,
            complete=True
        )

    def test_shows_normal_label_for_normal_level_in_present_tense(self):
        self.normal_smoking_history.smoking_current_response.value = True
        self.normal_smoking_history.smoking_current_response.save()

        form = SmokingFrequencyForm(
            tobacco_smoking_history=self.normal_smoking_history
        )
        self.assertEqual(
            form.fields["value"].label,
            f"How often do you smoke a pipe?"
        )

    def test_has_a_normal_label_for_normal_level_in_past_tense(self):
        self.normal_smoking_history.smoking_current_response.value = False
        self.normal_smoking_history.smoking_current_response.save()

        form = SmokingFrequencyForm(
            tobacco_smoking_history=self.normal_smoking_history
        )
        self.assertEqual(
            form.fields["value"].label,
            f"How often did you smoke a pipe?"
        )


    def test_shows_changed_label_for_changed_level(self):
        self.normal_smoking_history.smoked_amount_response.value = 10
        self.normal_smoking_history.smoked_amount_response.save()

        self.normal_smoking_history.smoking_frequency_response.value = SmokingFrequencyValues.WEEKLY.value
        self.normal_smoking_history.smoking_frequency_response.save()

        increased_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=self.normal_smoking_history.type,
            increased=True,
        )
        form = SmokingFrequencyForm(
            tobacco_smoking_history=increased_smoking_history,
            normal_tobacco_smoking_history=self.normal_smoking_history
        )

        self.assertEqual(
            form.fields["value"].label,
            f"When you smoked more than 10 full pipe loads a week, how often did you smoke a pipe?"
        )


    def test_is_valid_with_a_valid_value(self):
        form = SmokingFrequencyForm(
            tobacco_smoking_history=self.normal_smoking_history,
            data={
                "value": SmokingFrequencyValues.DAILY.value
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            SmokingFrequencyValues.DAILY.value
        )


    def test_has_a_required_error_message_for_normal_level_in_present_tense(self):
        self.normal_smoking_history.smoking_current_response.value = True
        self.normal_smoking_history.smoking_current_response.save()

        form = SmokingFrequencyForm(
            tobacco_smoking_history=self.normal_smoking_history,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            f"Select how often you smoke a pipe",
            form.errors["value"]
        )


    def test_has_a_normal_required_error_message_for_normal_level_in_past_tense(self):
        self.normal_smoking_history.smoking_current_response.value = False
        self.normal_smoking_history.smoking_current_response.save()

        form = SmokingFrequencyForm(
            tobacco_smoking_history=self.normal_smoking_history,
            data={
                "value": None
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            f"Select how often you smoked a pipe",
            form.errors["value"]
        )


    def test_has_a_required_error_message_for_changed_level(self):
        self.normal_smoking_history.smoked_amount_response.value = 10
        self.normal_smoking_history.smoked_amount_response.save()

        self.normal_smoking_history.smoking_frequency_response.value = SmokingFrequencyValues.WEEKLY.value
        self.normal_smoking_history.smoking_frequency_response.save()

        increased_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=self.normal_smoking_history.type,
            increased=True,
        )

        form = SmokingFrequencyForm(
            tobacco_smoking_history=increased_smoking_history,
            normal_tobacco_smoking_history=self.normal_smoking_history,
            data={
                "value": None
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            f"Select how often you smoked a pipe when you smoked more than 10 full pipe loads a week",
            form.errors["value"]
        )


    def test_is_invalid_with_a_non_numeric_value(self):
        form = SmokingFrequencyForm(
            tobacco_smoking_history=self.normal_smoking_history,
            data={
                "value": 'some string'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Select a valid choice. some string is not one of the available choices.",
            form.errors["value"]
        )
