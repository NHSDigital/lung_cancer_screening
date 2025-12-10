from django.test import TestCase

from ...factories.user_factory import UserFactory
from ....models.response_set import ResponseSet
from ....forms.respiratory_conditions_form import RespiratoryConditionsForm


class TestRespiratoryConditionsForm(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.response_set = ResponseSet(user=self.user)

    def test_is_valid_with_single_condition(self):
        form = RespiratoryConditionsForm(
            instance=self.response_set,
            data={
                "respiratory_conditions": ["P"]
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["respiratory_conditions"],
            ["P"]
        )

    def test_is_valid_with_multiple_conditions(self):
        form = RespiratoryConditionsForm(
            instance=self.response_set,
            data={
                "respiratory_conditions": ["P", "E", "C"]
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["respiratory_conditions"],
            ["P", "E", "C"]
        )

    def test_is_valid_with_none_of_the_above(self):
        form = RespiratoryConditionsForm(
            instance=self.response_set,
            data={
                "respiratory_conditions": ["N"]
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["respiratory_conditions"],
            ["N"]
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = RespiratoryConditionsForm(
            instance=self.response_set,
            data={
                "respiratory_conditions": ["invalid"]
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["respiratory_conditions"],
            ["Select a valid choice. invalid is not one of the available choices."]
        )

    def test_is_invalid_when_no_option_is_selected(self):
        form = RespiratoryConditionsForm(
            instance=self.response_set,
            data={
                "respiratory_conditions": []
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["respiratory_conditions"],
            ["Select if you have had any respiratory conditions"]
        )

    def test_is_invalid_with_none_of_the_above_selected_and_other_options_selected(
        self
    ):
        form = RespiratoryConditionsForm(
            instance=self.response_set,
            data={
                "respiratory_conditions": ["N", "P", "E", "C"]
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["respiratory_conditions"][0],
            (
                "Select if you have had any respiratory conditions, "
                "or select 'No, I have not had any of these "
                "respiratory conditions'"
            )
        )
