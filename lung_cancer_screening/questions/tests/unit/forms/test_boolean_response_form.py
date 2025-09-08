from django.test import TestCase
from ....forms.boolean_response_form import BooleanResponseForm

class TestBooleanResponseForm(TestCase):
    def test_is_valid(self):
        form = BooleanResponseForm(data={"value": True})
        self.assertTrue(form.is_valid())

    def test_is_invalid(self):
        form = BooleanResponseForm(data={"value": "invalid"})
        self.assertFalse(form.is_valid())

    def test_returns_a_boolean_type(self):
        form = BooleanResponseForm(data={"value": True})
        form.is_valid()
        self.assertIsInstance(form.cleaned_data["value"], bool)
