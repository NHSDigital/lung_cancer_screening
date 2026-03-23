from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory
from ...factories.smoked_amount_response_factory import SmokedAmountResponseFactory
from ...factories.smoking_frequency_response_factory import SmokingFrequencyResponseFactory

from ....forms.smoked_total_years_form import SmokedTotalYearsForm


@tag("SmokedTotalYears")
class TestSmokedTotalYearsForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory.create(eligible=True)
        self.age_when_started_smoking_response = AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.response_set
        )
        self.smoking_history = TobaccoSmokingHistoryFactory.create(
            cigarettes=True,
            complete=True,
            response_set=self.response_set
        )
        self.response = self.smoking_history.smoked_total_years_response

        self.valid_data = {
            "value": self.age_when_started_smoking_response.years_smoked_including_stopped() - 1
        }


    def test_has_a_normal_label_for_normal_type_in_present_tense(self):
        self.smoking_history.smoking_current_response.value = True
        self.smoking_history.smoking_current_response.save()

        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data=self.valid_data
        )
        self.assertEqual(
            form.label(),
            "Roughly how many years have you smoked cigarettes?",
        )


    def test_has_a_normal_label_for_normal_type_in_past_tense(self):
        self.smoking_history.smoking_current_response.value = False
        self.smoking_history.smoking_current_response.save()

        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data=self.valid_data
        )
        self.assertEqual(
            form.label(),
            "Roughly how many years did you smoke cigarettes?",
        )


    def test_has_a_changed_label_for_a_changed_level(self):
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


    def test_is_valid_with_a_valid_value(self):
        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data=self.valid_data
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            self.age_when_started_smoking_response.years_smoked_including_stopped() - 1
        )


    def test_has_a_required_error_message_for_a_normal_type_in_present_tense(self):
        self.smoking_history.smoking_current_response.value = True
        self.smoking_history.smoking_current_response.save()

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


    def test_has_a_required_error_message_for_a_normal_type_in_past_tense(self):
        self.smoking_history.smoking_current_response.value = False
        self.smoking_history.smoking_current_response.save()

        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Enter the number of years you smoked cigarettes",
            form.errors["value"]
        )


    def test_has_a_required_error_message_for_a_changed_level(self):
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
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Enter the number of years you smoked 200 cigarettes a week",
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


    def test_has_a_min_value_validation_for_a_normal_type(self):
        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data={
                "value": 0
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "The number of years you smoked cigarettes must be at least 1",
            form.errors["value"]
        )


    def test_has_a_min_value_validation_for_a_changed_level(self):
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
                "value": 0
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "The number of years you smoked 200 cigarettes a week must be at least 1",
            form.errors["value"]
        )


    def test_greater_than_years_smoked_for_normal_level(self):
        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data={
                "value": self.age_when_started_smoking_response.years_smoked_including_stopped() + 1
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "The number of years you smoked cigarettes must be equal to, or fewer than, the total number of years you smoked",
            form.errors["value"]
        )

    def test_greater_than_years_smoked_for_a_changed_level(self):
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
                "value": self.age_when_started_smoking_response.years_smoked_including_stopped() + 1
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(
            "The number of years you smoked 200 cigarettes a week must be equal to, or fewer than, the total number of years you have been smoking",
            form.errors["value"]
        )

    def test_page_title_for_a_normal_type(self):
        self.smoking_history.smoking_current_response.value = True
        self.smoking_history.smoking_current_response.save()

        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history
        )

        self.assertEqual(
            form.page_title(),
            "Number of years you have smoked cigarettes - NHS"
        )

    def test_page_title_for_a_changed_type(self):
        increased_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=self.smoking_history.type,
            increased=True
        )

        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=increased_smoking_history
        )

        self.assertEqual(
            form.page_title(),
            "Number of years you smoked cigarettes - NHS"
        )
