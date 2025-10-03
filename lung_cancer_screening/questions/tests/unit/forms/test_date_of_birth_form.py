from django.test import TestCase
from datetime import date

from ....models.participant import Participant
from ....forms.date_of_birth_form import DateOfBirthForm

class TestDateOfBirthForm(TestCase):
    def setUp(self):
        self.participant = Participant.objects.create(unique_id="1234567890")

    def test_is_valid_when_a_valid_date_is_provided(self):
        form = DateOfBirthForm(
            participant=self.participant,
            data={
                "date_of_birth_0": 1,
                "date_of_birth_1": 1,
                "date_of_birth_2": 2025
            }
        )
        self.assertTrue(form.is_valid())

    def test_is_invalid_when_no_date_is_provided(self):
        form = DateOfBirthForm(
            participant=self.participant,
            data={
                "date_of_birth_0": "",
                "date_of_birth_1": "",
                "date_of_birth_2": ""
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["date_of_birth"],
            ["Enter your date of birth."]
        )

    def test_is_invalid_when_a_partial_date_is_provided(self):
        form = DateOfBirthForm(
            participant=self.participant,
            data={
                "date_of_birth_0": "10",
                "date_of_birth_1": "",
                "date_of_birth_2": ""
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["date_of_birth"],
            ["Enter your full date of birth."]
        )

    def test_is_invalid_when_an_invalid_date_is_provided(self):
        form = DateOfBirthForm(
            participant=self.participant,
            data={
                "date_of_birth_0": "31",
                "date_of_birth_1": "02",
                "date_of_birth_2": "2025"
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["date_of_birth"],
            ["Date of birth must be a real date."]
        )

    def test_returns_a_date_type(self):
        form = DateOfBirthForm(
            participant=self.participant,
            data={
                "date_of_birth_0": 1,
                "date_of_birth_1": 1,
                "date_of_birth_2": 2025
            }
        )
        form.is_valid()
        self.assertIsInstance(form.cleaned_data["date_of_birth"], date)
