from django.test import TestCase, tag

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory

from ....models.smoking_current_response import SmokingCurrentResponse
from ....forms.smoking_current_form import SmokingCurrentForm


@tag("SmokingCurrent")
class TestSmokingCurrentForm(TestCase):
    def setUp(self):
        self.smoking_history = TobaccoSmokingHistoryFactory.create(
            medium_cigars=True
        )
        self.response = SmokingCurrentResponse.objects.create(
            tobacco_smoking_history=self.smoking_history,
            value=False
        )


    def test_is_valid_with_a_valid_value(self):
        form = SmokingCurrentForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data={
                "value": False
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            False
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = SmokingCurrentForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data={
                "value": "invalid"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select a valid choice. invalid is not one of the available choices."]
        )

    def test_is_invalid_when_no_option_is_selected(self):
        form = SmokingCurrentForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select if you currently smoke medium cigars"]
        )

    def test_label_contains_the_smoking_history_type(self):
        form = SmokingCurrentForm(
            instance=self.response,
            tobacco_smoking_history=self.smoking_history,
            data={
                "value": False
            }
        )
        self.assertEqual(
            form.fields["value"].label,
            "Do you currently smoke medium cigars?"
        )
