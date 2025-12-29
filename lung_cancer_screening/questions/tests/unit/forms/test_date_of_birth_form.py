from django.test import TestCase
from datetime import date

from ...factories.response_set_factory import ResponseSetFactory
from ....models.date_of_birth_response import DateOfBirthResponse
from ....forms.date_of_birth_form import DateOfBirthForm


class TestDateOfBirthForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.response = DateOfBirthResponse.objects.create(
            response_set=self.response_set,
            value=date(2000, 1, 1)
        )

    def test_is_valid_when_a_valid_date_is_provided(self):
        form = DateOfBirthForm(
            instance=self.response,
            data={
                "value_0": 1,
                "value_1": 1,
                "value_2": 2025
            }
        )
        self.assertTrue(form.is_valid())

    def test_is_invalid_when_no_date_is_provided(self):
        form = DateOfBirthForm(
            instance=self.response,
            data={
                "value_0": "",
                "value_1": "",
                "value_2": ""
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Enter your date of birth"]
        )

    def test_is_invalid_when_a_partial_date_is_provided(self):
        form = DateOfBirthForm(
            instance=self.response,
            data={
                "value_0": "10",
                "value_1": "",
                "value_2": ""
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Enter your full date of birth"]
        )

    def test_is_invalid_when_an_invalid_date_is_provided(self):
        form = DateOfBirthForm(
            instance=self.response,
            data={
                "value_0": "31",
                "value_1": "02",
                "value_2": "2025"
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Date of birth must be a real date"]
        )

    def test_returns_a_date_type(self):
        form = DateOfBirthForm(
            instance=self.response,
            data={
                "value_0": 1,
                "value_1": 1,
                "value_2": 2025
            }
        )
        form.is_valid()
        self.assertIsInstance(form.cleaned_data["value"], date)
