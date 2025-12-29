from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ....models.sex_at_birth_response import SexAtBirthResponse, SexAtBirthValues
from ....forms.sex_at_birth_form import SexAtBirthForm

class TestSexAtBirthForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.response = SexAtBirthResponse.objects.create(
            response_set=self.response_set,
            value=SexAtBirthValues.MALE
        )


    def test_is_valid_with_a_valid_value(self):
        form = SexAtBirthForm(
            instance=self.response,
            data={
                "value": SexAtBirthValues.FEMALE
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            SexAtBirthValues.FEMALE.value
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = SexAtBirthForm(
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
        form = SexAtBirthForm(
            instance=self.response,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select your sex at birth"]
        )
