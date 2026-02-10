from django.test import TestCase, tag

from ...factories.smoking_frequency_response_factory import SmokingFrequencyResponseFactory

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory

from ....models.smoking_frequency_response import SmokingFrequencyValues

@tag("SmokingFrequency")
class TestSmokingFrequencyResponse(TestCase):
    def setUp(self):
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory()

    def test_has_a_valid_factory(self):
        model = SmokingFrequencyResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history
        )
        model.full_clean()


    def test_has_tobacco_smoking_history_as_foreign_key(self):
        response = SmokingFrequencyResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=SmokingFrequencyValues.DAILY.value
        )

        self.assertEqual(response.tobacco_smoking_history, self.tobacco_smoking_history)

    def test_has_value_as_enum(self):
        response = SmokingFrequencyResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=SmokingFrequencyValues.DAILY.value
        )

        self.assertIsInstance(response.value, str)

    def test_get_value_display_as_singleton_text_returns_the_correct_text_daily(self):
        response = SmokingFrequencyResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=SmokingFrequencyValues.DAILY.value
        )
        self.assertEqual(response.get_value_display_as_singleton_text(), "day")


    def test_get_value_display_as_singleton_text_returns_the_correct_text_weekly(self):
        response = SmokingFrequencyResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=SmokingFrequencyValues.WEEKLY.value
        )
        self.assertEqual(response.get_value_display_as_singleton_text(), "week")


    def test_get_value_display_as_singleton_text_returns_the_correct_text_monthly(self):
        response = SmokingFrequencyResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=SmokingFrequencyValues.MONTHLY.value
        )
        self.assertEqual(response.get_value_display_as_singleton_text(), "month")
