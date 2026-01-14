from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ....models.relatives_age_when_diagnosed_response import RelativesAgeWhenDiagnosedResponse, RelativesAgeWhenDiagnosedValues
from ....forms.relatives_age_when_diagnosed_form import RelativesAgeWhenDiagnosedForm

@tag("RelativesAgeWhenDiagnosed")
class TestRelativesLungCancerForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.response = RelativesAgeWhenDiagnosedResponse.objects.create(
            response_set=self.response_set,
            value=RelativesAgeWhenDiagnosedValues.NO
        )


    def test_is_valid_with_a_valid_value(self):
        form = RelativesAgeWhenDiagnosedForm(
            instance=self.response,
            data={
                "value": RelativesAgeWhenDiagnosedValues.NO
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            RelativesAgeWhenDiagnosedValues.NO
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = RelativesAgeWhenDiagnosedForm(
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
        form = RelativesAgeWhenDiagnosedForm(
            instance=self.response,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select if your relatives were younger than 60 when they were diagnosed with lung cancer"]
        )
