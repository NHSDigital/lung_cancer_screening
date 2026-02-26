from django.test import TestCase, tag

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.smoked_total_years_response_factory import SmokedTotalYearsResponseFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory
from ....models.tobacco_smoking_history import TobaccoSmokingHistoryTypes, TobaccoSmokingHistory
from ....forms.smoked_total_years_form import SmokedTotalYearsForm


@tag("SmokedTotalYears")
class TestSmokedTotalYearsForm(TestCase):
    def setUp(self):
        self.smoking_history = TobaccoSmokingHistoryFactory.create(
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
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

    def has_a_customised_label_for_a_non_normal_type(self):
        self.smoking_history.level = TobaccoSmokingHistory.Levels.INCREASED
        self.smoking_history.save()

        form = SmokedTotalYearsForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data=self.valid_data
        )
        self.assertEqual(
            form.label(),
            "Roughly how many years did you smoke 200 cigarettes a week?"
        )
