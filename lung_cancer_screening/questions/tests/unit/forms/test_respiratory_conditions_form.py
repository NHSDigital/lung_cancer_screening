from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ....models.respiratory_conditions_response import RespiratoryConditionsResponse
from ....forms.respiratory_conditions_form import RespiratoryConditionsForm


class TestRespiratoryConditionsForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.response = RespiratoryConditionsResponse.objects.create(
            response_set=self.response_set,
            value=["P"]
        )

    def test_is_valid_with_single_condition(self):
        form = RespiratoryConditionsForm(
            instance=self.response,
            data={
                "value": ["P"]
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            ["P"]
        )

    def test_is_valid_with_multiple_conditions(self):
        form = RespiratoryConditionsForm(
            instance=self.response,
            data={
                "value": ["P", "E", "C"]
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            ["P", "E", "C"]
        )

    def test_is_valid_with_none_of_the_above(self):
        form = RespiratoryConditionsForm(
            instance=self.response,
            data={
                "value": ["N"]
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            ["N"]
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = RespiratoryConditionsForm(
            instance=self.response,
            data={
                "value": ["invalid"]
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select a valid choice. invalid is not one of the available choices."]
        )

    def test_is_invalid_when_no_option_is_selected(self):
        form = RespiratoryConditionsForm(
            instance=self.response,
            data={
                "value": []
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select if you have had any respiratory conditions"]
        )

    def test_is_invalid_with_none_of_the_above_selected_and_other_options_selected(
        self
    ):
        form = RespiratoryConditionsForm(
            instance=self.response,
            data={
                "value": ["N", "P", "E", "C"]
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"][0],
            (
                "Select if you have had any respiratory conditions, "
                "or select 'No, I have not had any of these "
                "respiratory conditions'"
            )
        )
