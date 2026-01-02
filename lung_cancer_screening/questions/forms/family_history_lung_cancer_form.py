from django import forms

from ...nhsuk_forms.choice_field import ChoiceField
from ..models.family_history_lung_cancer_response import FamilyHistoryLungCancerResponse, FamilyHistoryLungCancerValues


class FamilyHistoryLungCancerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = ChoiceField(
            choices=FamilyHistoryLungCancerValues.choices,
            label="Have any of your parents, siblings or children ever been diagnosed with lung cancer?",
            widget=forms.RadioSelect,
            error_messages={
                'required': 'Select if any of your parents, siblings or children have had a diagnosis of lung cancer'
            }
        )

    class Meta:
        model = FamilyHistoryLungCancerResponse
        fields = ['value']
