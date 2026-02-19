from django.test import TestCase, tag

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.smoking_current_response_factory import SmokingCurrentResponseFactory
from ...factories.smoked_amount_response_factory import SmokedAmountResponseFactory
from ...factories.smoking_frequency_response_factory import SmokingFrequencyResponseFactory
from ....models.tobacco_smoking_history import TobaccoSmokingHistoryTypes
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

    def test_label_has_the_correct_type(self):
        cigarettes_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=TobaccoSmokingHistoryTypes.CIGARETTES.value
        )
        SmokingCurrentResponseFactory.create(
            tobacco_smoking_history=cigarettes_smoking_history
        )
        cigars_smoking_history = TobaccoSmokingHistoryFactory.create(
            type=TobaccoSmokingHistoryTypes.CIGARS.value
        )
        cigarettes_response = SmokedAmountResponseFactory.create(
            tobacco_smoking_history=cigarettes_smoking_history
        )
        cigars_response = SmokedAmountResponseFactory.create(
            tobacco_smoking_history=cigars_smoking_history
        )
        SmokingCurrentResponseFactory.create(
            tobacco_smoking_history=cigars_smoking_history
        )
        cigarettes_form = SmokedAmountForm(
            instance=cigarettes_response,
            data={"value": 20}
        )
        cigars_form = SmokedAmountForm(
            instance=cigars_response,
            data={"value": 20}
        )
        self.assertIn("cigarettes", cigarettes_form.fields["value"].label)
        self.assertIn("cigars", cigars_form.fields["value"].label)


    def test_label_has_the_correct_frequency(self):
        form = SmokedAmountForm(
            instance=self.response,
            data={"value": 20},
            frequency_text="my frequency"
        )

        self.assertIn("my frequency", form.fields["value"].label)


    def test_label_has_the_correct_currently_or_previously_text(self):
        form = SmokedAmountForm(
            instance=self.response,
            data={"value": 20},
        )

        self.assertIn("previously", form.fields["value"].label)


    def test_min_value_validation_has_the_correct_message(self):
        self.smoking_history.type = TobaccoSmokingHistoryTypes.CIGARS.value
        self.smoking_history.save()

        form = SmokedAmountForm(
            instance=self.response,
            data={"value": 0}
        )
        form.full_clean()
        self.assertIn("value", form.errors)
        self.assertIn(
            "The number of cigars you smoke must be at least 1",
            form.errors["value"],
        )
