from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ....models.family_history_lung_cancer_response import FamilyHistoryLungCancerResponse, FamilyHistoryLungCancerValues
from ....forms.family_history_lung_cancer_form import FamilyHistoryLungCancerForm

@tag("FamilyHistoryLungCancer")
class TestFamilyHistoryLungCancerForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.response = FamilyHistoryLungCancerResponse.objects.create(
            response_set=self.response_set,
            value=FamilyHistoryLungCancerValues.NO
        )


    def test_is_valid_with_a_valid_value(self):
        form = FamilyHistoryLungCancerForm(
            instance=self.response,
            data={
                "value": FamilyHistoryLungCancerValues.NO
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            FamilyHistoryLungCancerValues.NO
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = FamilyHistoryLungCancerForm(
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
        form = FamilyHistoryLungCancerForm(
            instance=self.response,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select if any of your parents, siblings or children have had a diagnosis of lung cancer"]
        )
