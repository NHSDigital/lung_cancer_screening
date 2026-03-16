from django.test import TestCase, tag

from ....models.terms_of_use_response import TermsOfUseResponse

from ...factories.response_set_factory import ResponseSetFactory
from ....forms.agree_terms_of_use_form import TermsOfUseForm

@tag("TermsOfUse")
class TestAgreeTermsOfUseForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.response = TermsOfUseResponse.objects.create(
            response_set=self.response_set,
            value=False
        )


    def test_is_valid_with_a_valid_value(self):
        form = TermsOfUseForm(
            instance=self.response,
            data={
                "value": ["True"]
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.data["value"],
            ["True"]
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = TermsOfUseForm(
            instance=self.response,
            data={
                "value": "Invalid entry"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Agree to the terms of use to continue"]
        )

    def test_is_invalid_when_no_option_is_selected(self):
        form = TermsOfUseForm(
            instance=self.response,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Agree to the terms of use to continue"]
        )
