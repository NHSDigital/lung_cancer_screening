from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ....models.education_response import EducationResponse, EducationValues
from ....forms.education_form import EducationForm


@tag("Education")
class TestEducationForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.response = EducationResponse.objects.create(
            response_set=self.response_set,
            value=[EducationValues.GCSES]
        )

    def test_is_valid_with_a_valid_value(self):
        form = EducationForm(
            instance=self.response,
            data={
                'value': [EducationValues.GCSES]
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data['value'],
            [EducationValues.GCSES]
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = EducationForm(
            instance=self.response,
            data={
                "value": ["invalid"]
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select a valid choice. invalid is not one of the available choices."]
        )

    def test_is_invalid_when_no_option_is_selected(self):
        form = EducationForm(
            instance=self.response,
            data={
                "value": []
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select your level of education"]
        )
