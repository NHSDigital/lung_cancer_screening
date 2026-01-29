from django.test import TestCase, tag

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.smoked_total_years_response_factory import SmokedTotalYearsResponseFactory
from ....models.tobacco_smoking_history import TobaccoSmokingHistoryTypes
from ....forms.smoked_total_years_form import SmokedTotalYearsForm


@tag("SmokedTotalYears")
class TestSmokedTotalYearsForm(TestCase):
    def setUp(self):
        self.smoking_history = TobaccoSmokingHistoryFactory.create(
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )
        self.response = SmokedTotalYearsResponseFactory.build(
            tobacco_smoking_history=self.smoking_history
        )


    def test_is_valid_with_a_valid_value(self):
        form = SmokedTotalYearsForm(
            instance=self.response,
            data={
                "value": 10
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            10
        )

    def test_is_invalid_with_a_none_value(self):
        form = SmokedTotalYearsForm(
            instance=self.response,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Enter the number of years you have smoked cigarettes"]
        )

    def test_is_invalid_with_a_non_numeric_value(self):
        form = SmokedTotalYearsForm(
            instance=self.response,
            data={
                "value": 'some string'
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Years must be in whole numbers"]
        )
