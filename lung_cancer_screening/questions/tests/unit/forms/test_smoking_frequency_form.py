from django.test import TestCase, tag

from lung_cancer_screening.questions.forms.smoking_frequency_form import SmokingFrequencyForm
from lung_cancer_screening.questions.models.smoking_frequency_response import SmokingFrequencyValues
from lung_cancer_screening.questions.tests.factories.response_set_factory import ResponseSetFactory

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory


@tag("SmokingFrequency")
class TestSmokingFrequencyForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory.create(complete=True)
        self.normal_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            normal=True,
            cigarillos=True,
            complete=True
        )


    def test_is_valid_with_a_valid_value(self):
        form = SmokingFrequencyForm(
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
            tobacco_smoking_history_item=self.normal_smoking_history,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            f"Select how often you smoke {self.normal_smoking_history.human_type().lower()}",
            form.errors["value"]
        )


    def test_is_invalid_with_a_non_numeric_value(self):
        form = SmokingFrequencyForm(
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
            tobacco_smoking_history_item=self.normal_smoking_history
        )
        self.assertEqual(
            form.fields["value"].label,
            f"How often do you smoke {self.normal_smoking_history.human_type().lower()}?"
        )

    def test_shows_increased_label_for_increased_level(self):
        increased_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=self.normal_smoking_history.type,
            increased=True,
        )
        form = SmokingFrequencyForm(
            tobacco_smoking_history_item=increased_smoking_history,
            normal_tobacco_smoking_history_item=self.normal_smoking_history
        )
        self.assertEqual(
            form.fields["value"].label,
            f"When you smoked more than {self.get_normal_smoking_string()}, how often did you smoke {self.normal_smoking_history.human_type().lower()}?"
        )

    def get_normal_smoking_string(self):
        amount = self.normal_smoking_history.smoked_amount_response
        frequency = self.normal_smoking_history.smoking_frequency_response
        return f"{amount.value} {self.normal_smoking_history.human_type().lower()} a {frequency.get_value_display_as_singleton_text()}"


    def test_has_a_required_error_message(self):
        form = SmokingFrequencyForm(
            tobacco_smoking_history_item=self.normal_smoking_history,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            f"Select how often you smoke {self.normal_smoking_history.human_type().lower()}",
            form.errors["value"]
        )

    def test_has_a_changed_required_error_message(self):
        self.normal_smoking_history.smoked_amount_response.value = 10
        self.normal_smoking_history.smoked_amount_response.save()

        self.normal_smoking_history.smoking_frequency_response.value = SmokingFrequencyValues.DAILY.value
        self.normal_smoking_history.smoking_frequency_response.save()

        increased_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=self.normal_smoking_history.type,
            increased=True,
        )

        form = SmokingFrequencyForm(
            tobacco_smoking_history_item=increased_smoking_history,
            normal_tobacco_smoking_history_item=self.normal_smoking_history,
            data={
                "value": None
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            (
                f"Select how often you smoked {self.normal_smoking_history.human_type().lower()} "
                "when you smoked more than 10 "
                f"{self.normal_smoking_history.unit()} a day"
            ),
            form.errors["value"]
        )
