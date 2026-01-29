from django.test import TestCase, tag

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.smoked_amount_response_factory import SmokedAmountResponseFactory
from ....models.tobacco_smoking_history import TobaccoSmokingHistoryTypes
from ....forms.smoked_amount_form import SmokedAmountForm


@tag("SmokedAmount")
class TestSmokedAmountForm(TestCase):
    def setUp(self):
        self.smoking_history = TobaccoSmokingHistoryFactory.create(
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )
        self.response = SmokedAmountResponseFactory.build(
            tobacco_smoking_history=self.smoking_history
        )

    def test_is_valid_with_a_valid_value(self):
        form = SmokedAmountForm(
            instance=self.response,
            data={"value": 20}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["value"], 20)

    def test_is_invalid_with_a_none_value(self):
        form = SmokedAmountForm(
            instance=self.response,
            data={"value": None}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("value", form.errors)

    def test_is_invalid_with_a_non_numeric_value(self):
        form = SmokedAmountForm(
            instance=self.response,
            data={"value": "not a number"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("value", form.errors)
