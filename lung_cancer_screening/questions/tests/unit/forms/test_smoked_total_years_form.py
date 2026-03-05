from django.test import TestCase, tag

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.smoked_total_years_response_factory import SmokedTotalYearsResponseFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory
from ...factories.smoked_amount_response_factory import SmokedAmountResponseFactory
from ...factories.smoking_frequency_response_factory import SmokingFrequencyResponseFactory

from ....forms.smoked_total_years_form import SmokedTotalYearsForm


@tag("SmokedTotalYears", "wip")
class TestSmokedTotalYearsForm(TestCase):
    def setUp(self):
        self.smoking_history = TobaccoSmokingHistoryFactory.create(
            cigarettes=True
        )
        self.age_started_smoking_response = AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.smoking_history.response_set
        )
        self.response = SmokedTotalYearsResponseFactory.build(
            tobacco_smoking_history=self.smoking_history
        )

        self.valid_data = {
            "value": self.age_started_smoking_response.years_smoked_including_stopped() - 1
        }


    def test_is_valid_with_a_valid_value(self):
        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data=self.valid_data
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            self.age_started_smoking_response.years_smoked_including_stopped() - 1
        )

    def test_is_invalid_with_a_none_value(self):
        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Enter the number of years you have smoked cigarettes",
            form.errors["value"]
        )


    def test_is_invalid_with_a_non_numeric_value(self):
        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data={
                "value": 'some string'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Years must be in whole numbers",
            form.errors["value"]
        )

    def test_has_a_default_label_for_normal_type(self):
        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data=self.valid_data
        )
        self.assertEqual(
            form.label(),
            "Roughly how many years have you smoked cigarettes?",
        )

    def test_has_a_customised_label_for_a_non_normal_type(self):
        increased_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=self.smoking_history.type,
            increased=True
        )
        SmokedAmountResponseFactory.create(
            tobacco_smoking_history=increased_smoking_history,
            value=200
        )
        SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=increased_smoking_history,
            weekly=True
        )

        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=increased_smoking_history,
            data=self.valid_data
        )

        self.assertEqual(
            form.label(),
            "Roughly how many years did you smoke 200 cigarettes a week?"
        )


    def test_has_a_required_error_message_including_the_type_of_tobacco_smoking_history(self):
        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data={
                "value": None
            }
        )
        self.assertIn(
            "Enter the number of years you have smoked cigarettes",
            form.errors["value"]
        )


    def test_has_a_required_error_message_including_the_unit_of_the_tobacco_smoking_history(self):
        increased_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=self.smoking_history.type,
            increased=True
        )
        SmokedAmountResponseFactory.create(
            tobacco_smoking_history=increased_smoking_history,
            value=200
        )
        SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=increased_smoking_history,
            weekly=True
        )


        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=increased_smoking_history,
            data={
                "value": None
            }
        )

        self.assertIn(
            "Enter the number of years you have smoked 200 cigarettes a week",
            form.errors["value"]
        )
