from django.test import TestCase

from ...factories.user_factory import UserFactory
from ....models.response_set import ResponseSet, GenderValues
from ....forms.gender_form import GenderForm


class TestGenderForm(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.response_set = ResponseSet(user=self.user)

    def test_is_valid_with_a_valid_value(self):
        form = GenderForm(
            instance=self.response_set,
            data={
                "gender": GenderValues.MALE
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["gender"],
            GenderValues.MALE.value
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = GenderForm(
            instance=self.response_set,
            data={
                "gender": "invalid"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["gender"],
            ["Select a valid choice. invalid is not one of the available choices."]
        )

    def test_is_invalid_when_no_option_is_selected(self):
        form = GenderForm(
            instance=self.response_set,
            data={
                "gender": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["gender"],
            ["Select the option that best describes your gender"]
        )
