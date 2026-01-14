from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ....models.gender_response import GenderResponse, GenderValues
from ....forms.gender_form import GenderForm


@tag("Gender")
class TestGenderForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.response = GenderResponse.objects.create(
            response_set=self.response_set,
            value=GenderValues.MALE
        )

    def test_is_valid_with_a_valid_value(self):
        form = GenderForm(
            instance=self.response,
            data={
                "value": GenderValues.MALE
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            GenderValues.MALE.value
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = GenderForm(
            instance=self.response,
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
        form = GenderForm(
            instance=self.response,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select the option that best describes your gender"]
        )
