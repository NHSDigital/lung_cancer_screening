from django.test import TestCase

from ...factories.user_factory import UserFactory
from ....models.response_set import ResponseSet, SexAtBirthValues
from ....forms.sex_at_birth_form import SexAtBirthForm

class TestSexAtBirthForm(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.response_set = ResponseSet(user=self.user)


    def test_is_valid_with_a_valid_value(self):
        form = SexAtBirthForm(
            instance=self.response_set,
            data={
                "sex_at_birth": SexAtBirthValues.FEMALE
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["sex_at_birth"],
            SexAtBirthValues.FEMALE.value
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = SexAtBirthForm(
            instance=self.response_set,
            data={
                "sex_at_birth": "invalid"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["sex_at_birth"],
            ["Select a valid choice. invalid is not one of the available choices."]
        )

    def test_is_invalid_when_no_option_is_selected(self):
        form = SexAtBirthForm(
            instance=self.response_set,
            data={
                "sex_at_birth": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["sex_at_birth"],
            ["Select your sex at birth"]
        )
