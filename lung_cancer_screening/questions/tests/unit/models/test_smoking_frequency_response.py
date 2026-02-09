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
