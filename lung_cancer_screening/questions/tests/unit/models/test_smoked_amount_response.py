from django.test import TestCase, tag

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.smoked_amount_response_factory import SmokedAmountResponseFactory
from ....models.tobacco_smoking_history import TobaccoSmokingHistoryTypes


@tag("SmokedAmount")
class TestSmokedAmountResponse(TestCase):
    def setUp(self):
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )

    def test_has_a_valid_factory(self):
        model = SmokedAmountResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history
        )
        model.full_clean()

    def test_has_tobacco_smoking_history_as_foreign_key(self):
        response = SmokedAmountResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history
        )
        self.assertEqual(response.tobacco_smoking_history, self.tobacco_smoking_history)

    def test_has_value_as_integer(self):
        response = SmokedAmountResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=15
        )
        self.assertEqual(response.value, 15)
