from django.test import TestCase
from datetime import date

from ....forms.date_of_birth_form import DateOfBirthForm

class TestDateOfBirthForm(TestCase):
    def test_is_valid(self):
        form = DateOfBirthForm(data={
            "date_of_birth_0": 1,
            "date_of_birth_1": 1,
            "date_of_birth_2": 2025
        })
        self.assertTrue(form.is_valid())

    def test_is_invalid(self):
        form = DateOfBirthForm(data={
            "date_of_birth_0": 100,
            "date_of_birth_1": 100,
            "date_of_birth_2": 2025
        })

        self.assertFalse(form.is_valid())

    def test_returns_a_date_type(self):
        form = DateOfBirthForm(data={
            "date_of_birth_0": 1,
            "date_of_birth_1": 1,
            "date_of_birth_2": 2025
        })
        form.is_valid()
        self.assertIsInstance(form.cleaned_data["date_of_birth"], date)
