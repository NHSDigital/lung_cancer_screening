from django.test import TestCase, tag
from django.core.exceptions import ValidationError

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

    def test_is_invalid_if_value_is_less_than_1(self):
        response = SmokedAmountResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=0
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn("value", context.exception.message_dict)
        self.assertIn(
            "Ensure this value is greater than or equal to 1.",
            context.exception.message_dict["value"],
        )
