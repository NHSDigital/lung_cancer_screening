from django import forms
from ...nhsuk_forms.typed_choice_field import TypedChoiceField
from ..models.cancer_diagnosis_response import CancerDiagnosisResponse


class CancerDiagnosisForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = TypedChoiceField(
            choices=[(True, "Yes"), (False, "No")],
            widget=forms.RadioSelect,
            label="Have you ever been diagnosed with cancer?",
            label_classes="nhsuk-fieldset__legend--m",
            coerce=lambda x: x == "True",
            error_messages={
                "required": "Select if you have been diagnosed with cancer"
            },
        )

    class Meta:
        model = CancerDiagnosisResponse
        fields = ['value']
