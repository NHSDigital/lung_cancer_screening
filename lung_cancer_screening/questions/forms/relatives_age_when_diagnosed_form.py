from django import forms

from ...nhsuk_forms.choice_field import ChoiceField
from ..models.relatives_age_when_diagnosed_response import RelativesAgeWhenDiagnosedResponse, RelativesAgeWhenDiagnosedValues


class RelativesAgeWhenDiagnosedForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = ChoiceField(
            choices=RelativesAgeWhenDiagnosedValues.choices,
            label="Were any of your relatives younger than 60 years old when they were diagnosed with lung cancer?",
            widget=forms.RadioSelect,
            error_messages={
                'required': 'Select if your relatives were younger than 60 when they were diagnosed with lung cancer'
            }
        )

    class Meta:
        model = RelativesAgeWhenDiagnosedResponse
        fields = ['value']
