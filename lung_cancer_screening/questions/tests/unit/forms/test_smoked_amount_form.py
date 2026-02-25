from django.test import TestCase, tag

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.smoking_current_response_factory import SmokingCurrentResponseFactory
from ...factories.smoked_amount_response_factory import SmokedAmountResponseFactory
from ...factories.smoking_frequency_response_factory import SmokingFrequencyResponseFactory
from ....models.tobacco_smoking_history import TobaccoSmokingHistoryTypes, TobaccoSmokingHistory
from ....models.smoking_frequency_response import SmokingFrequencyValues
from ....forms.smoked_amount_form import SmokedAmountForm


@tag("SmokedAmount")
class TestSmokedAmountForm(TestCase):
    def setUp(self):
        self.smoking_history = TobaccoSmokingHistoryFactory.create(
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )
        self.smoking_current_response = SmokingCurrentResponseFactory.create(
            tobacco_smoking_history=self.smoking_history,
            value=False
        )
        self.frequency_response = SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=self.smoking_history,
            value=SmokingFrequencyValues.DAILY
        )
        self.response = SmokedAmountResponseFactory.build(
            tobacco_smoking_history=self.smoking_history
        )

    def test_is_valid_with_a_valid_value(self):
        form = SmokedAmountForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data={"value": 20}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["value"], 20)

    def test_is_invalid_with_a_none_value(self):
        form = SmokedAmountForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data={"value": None}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("value", form.errors)

    def test_is_invalid_with_a_non_numeric_value(self):
        form = SmokedAmountForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data={"value": "not a number"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("value", form.errors)


    def test_min_value_validation_has_the_correct_message(self):
        self.smoking_history.type = TobaccoSmokingHistoryTypes.CIGARS.value
        self.smoking_history.save()

        form = SmokedAmountForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data={"value": 0}
        )
        form.full_clean()
        self.assertIn("value", form.errors)
        self.assertIn(
            "The number of cigars you smoke must be at least 1",
            form.errors["value"],
        )


    def test_has_a_label_for_the_normal_type(self):
        form = SmokedAmountForm(
            instance=self.response,
            data={"value": 20},
            tobacco_smoking_history=self.smoking_history
        )

        self.assertEqual(
            form.fields["value"].label,
            "Roughly how many cigarettes do you previously smoke in a normal day?"
        )


    def test_has_a_label_for_the_increased_type(self):
        increased_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            level=TobaccoSmokingHistory.Levels.INCREASED
        )
        SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=increased_smoking_history,
            value=SmokingFrequencyValues.DAILY
        )

        form = SmokedAmountForm(
            instance=self.response,
            data={"value": 20},
            tobacco_smoking_history=increased_smoking_history,
            normal_tobacco_smoking_history=self.smoking_history
        )

        self.assertEqual(
            form.fields["value"].label,
            "When you smoked more than 20 cigarettes a day, roughly how many cigarettes did you normally smoke a day?"
        )


    def test_has_a_label_for_the_decreased_type(self):
        decreased_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            level=TobaccoSmokingHistory.Levels.DECREASED
        )
        SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=decreased_smoking_history,
            value=SmokingFrequencyValues.DAILY
        )

        form = SmokedAmountForm(
            instance=self.response,
            data={"value": 20},
            tobacco_smoking_history=decreased_smoking_history,
            normal_tobacco_smoking_history=self.smoking_history
        )

        self.assertEqual(
            form.fields["value"].label,
            "When you smoked fewer than 20 cigarettes a day, roughly how many cigarettes did you normally smoke a day?"
        )


    def test_has_a_required_error_message_for_the_normal_type(self):
        form = SmokedAmountForm(
            instance=self.response,
            data={"value": None},
            tobacco_smoking_history=self.smoking_history
        )

        form.full_clean()
        self.assertIn("value", form.errors)
        self.assertIn(
            "Enter how many cigarettes you previously smoke in a normal day",
            form.errors["value"],
        )

    def test_has_a_required_error_message_for_the_increased_type(self):
        increased_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            level=TobaccoSmokingHistory.Levels.INCREASED
        )
        SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=increased_smoking_history,
            value=SmokingFrequencyValues.DAILY
        )

        form = SmokedAmountForm(
            instance=self.response,
            data={"value": None},
            tobacco_smoking_history=increased_smoking_history,
            normal_tobacco_smoking_history=self.smoking_history
        )

        form.full_clean()
        self.assertIn("value", form.errors)
        self.assertIn(
            "Enter the number of cigarettes you smoked when you smoked more than 20 cigarettes a day",
            form.errors["value"],
        )

    def test_has_a_required_error_message_for_the_decreased_type(self):
        decreased_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value,
            level=TobaccoSmokingHistory.Levels.DECREASED
        )
        SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=decreased_smoking_history,
            value=SmokingFrequencyValues.DAILY
        )

        form = SmokedAmountForm(
            instance=self.response,
            data={"value": None},
            tobacco_smoking_history=decreased_smoking_history,
            normal_tobacco_smoking_history=self.smoking_history
        )

        form.full_clean()
        self.assertIn("value", form.errors)
        self.assertIn(
            "Enter the number of cigarettes you smoked when you smoked fewer than 20 cigarettes a day",
            form.errors["value"],
        )
