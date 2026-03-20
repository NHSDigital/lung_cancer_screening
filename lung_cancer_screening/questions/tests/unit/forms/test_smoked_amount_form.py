from django.test import TestCase, tag

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.smoking_current_response_factory import SmokingCurrentResponseFactory
from ...factories.smoked_amount_response_factory import SmokedAmountResponseFactory
from ...factories.smoking_frequency_response_factory import SmokingFrequencyResponseFactory
from ....forms.smoked_amount_form import SmokedAmountForm


@tag("SmokedAmount")
class TestSmokedAmountForm(TestCase):
    def setUp(self):
        self.smoking_history = TobaccoSmokingHistoryFactory.create(
            pipe=True
        )
        self.smoking_current_response = SmokingCurrentResponseFactory.create(
            tobacco_smoking_history=self.smoking_history,
            value=False
        )
        self.frequency_response = SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=self.smoking_history,
            daily=True
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


    def test_min_value_validation_for_normal_level(self):
        form = SmokedAmountForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data={"value": 0}
        )
        form.full_clean()
        self.assertIn("value", form.errors)
        self.assertIn(
            "The number of full pipe loads you smoked a day must be at least 1",
            form.errors["value"],
        )


    def test_min_value_validation_for_changed_level(self):
        increased_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=self.smoking_history.type,
            increased=True
        )
        SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=increased_smoking_history,
            daily=True
        )
        form = SmokedAmountForm(
            instance=self.response,
            tobacco_smoking_history=increased_smoking_history,
            normal_tobacco_smoking_history=self.smoking_history,
            data={"value": 0}
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            f"The number of {increased_smoking_history.unit()} you smoked a day must be at least 1",
            form.errors["value"],
        )

    def test_has_a_label_for_the_normal_type_for_current_smoking_history(self):
        self.smoking_current_response.value = True
        self.smoking_current_response.save()

        form = SmokedAmountForm(
            instance=self.response,
            data={"value": 20},
            tobacco_smoking_history=self.smoking_history
        )

        self.assertEqual(
            form.fields["value"].label,
            "Roughly how many full pipe loads do you currently smoke in a normal day?"
        )


    def test_has_a_label_for_the_normal_type_for_non_current_smoking_history(self):
        self.smoking_current_response.value = False
        self.smoking_current_response.save()

        form = SmokedAmountForm(
            instance=self.response,
            data={"value": 20},
            tobacco_smoking_history=self.smoking_history
        )
        self.assertEqual(
            form.fields["value"].label,
            "Roughly how many full pipe loads did you normally smoke a day?"
        )


    def test_has_a_label_for_the_increased_type(self):
        increased_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=self.smoking_history.type,
            increased=True
        )
        SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=increased_smoking_history,
            daily=True
        )

        form = SmokedAmountForm(
            instance=self.response,
            data={"value": 20},
            tobacco_smoking_history=increased_smoking_history,
            normal_tobacco_smoking_history=self.smoking_history
        )

        self.assertEqual(
            form.fields["value"].label,
            "When you smoked more than 20 full pipe loads a day, roughly how many full pipe loads did you normally smoke a day?"
        )


    def test_has_a_label_for_the_decreased_type(self):
        decreased_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=self.smoking_history.type,
            decreased=True
        )
        SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=decreased_smoking_history,
            daily=True
        )

        form = SmokedAmountForm(
            instance=self.response,
            data={"value": 20},
            tobacco_smoking_history=decreased_smoking_history,
            normal_tobacco_smoking_history=self.smoking_history
        )

        self.assertEqual(
            form.fields["value"].label,
            "When you smoked fewer than 20 full pipe loads a day, roughly how many full pipe loads did you normally smoke a day?"
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
            "Enter how many full pipe loads you previously smoked in a normal day",
            form.errors["value"],
        )

    def test_has_a_required_error_message_for_the_increased_type(self):
        increased_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=self.smoking_history.type,
            increased=True
        )
        SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=increased_smoking_history,
            daily=True
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
            "Enter the number of full pipe loads you smoked when you smoked more than 20 full pipe loads a day",
            form.errors["value"],
        )

    def test_has_a_required_error_message_for_the_decreased_type(self):
        decreased_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=self.smoking_history.type,
            decreased=True
        )
        SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=decreased_smoking_history,
            daily=True
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
            "Enter the number of full pipe loads you smoked when you smoked fewer than 20 full pipe loads a day",
            form.errors["value"],
        )

def test_has_correct_page_title_for_changed_level(self):
        increased_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=self.smoking_history.type,
            increased=True,
        )

        form = SmokedAmountForm(
            tobacco_smoking_history=increased_smoking_history,
            normal_tobacco_smoking_history=self.smoking_history,
        )

        self.assertEqual(
            form.page_title(),
            "Number of full pipe loads you normally smoked when your smoking increased"
        )
