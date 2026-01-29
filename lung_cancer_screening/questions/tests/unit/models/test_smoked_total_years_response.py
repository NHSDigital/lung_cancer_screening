from django.test import TestCase, tag

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.smoked_total_years_response_factory import SmokedTotalYearsResponseFactory


@tag("SmokedTotalYears")
class TestSmokedTotalYearsResponse(TestCase):
    def setUp(self):
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory()

    def test_has_a_valid_factory(self):
        model = SmokedTotalYearsResponseFactory.build(tobacco_smoking_history=self.tobacco_smoking_history)
        model.full_clean()


    def test_has_tobacco_smoking_history_as_foreign_key(self):
        response = SmokedTotalYearsResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=10
        )

        self.assertEqual(response.tobacco_smoking_history, self.tobacco_smoking_history)

    def test_has_value_as_int(self):
        response = SmokedTotalYearsResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=10
        )

        self.assertIsInstance(response.value, int)
