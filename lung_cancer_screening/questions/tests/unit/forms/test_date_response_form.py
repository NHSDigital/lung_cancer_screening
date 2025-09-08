from django.test import TestCase
from datetime import date

from ....forms.date_response_form import DateResponseForm

class TestDateResponseForm(TestCase):
    def test_date_response_form_is_valid(self):
        form = DateResponseForm(data={
            "value_0": 1,
            "value_1": 1,
            "value_2": 2025
        })
        self.assertTrue(form.is_valid())

    def test_date_response_form_is_invalid(self):
        form = DateResponseForm(data={
            "value_0": 100,
            "value_1": 100,
            "value_2": 2025
        })
        self.assertFalse(form.is_valid())

    def test_returns_a_date_type(self):
        form = DateResponseForm(data={
            "value_0": 1,
            "value_1": 1,
            "value_2": 2025
        })
        form.is_valid()
        self.assertIsInstance(form.cleaned_data["value"], date)
