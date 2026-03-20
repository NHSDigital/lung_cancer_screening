from django import forms

from ...nhsuk_forms.choice_field import ChoiceField
from ..models.gender_response import GenderResponse, GenderValues


class GenderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = ChoiceField(
            choices=GenderValues.choices,
            widget=forms.RadioSelect,
            label="Which of these best describes you?",
            error_messages={
                'required': 'Select the option that best describes your gender'
            }
        )

        # Add divider before "PREFER_NOT_TO_SAY"
        fields = self["value"]
        fields.add_divider_after(
            GenderValues.NON_BINARY,
            "or"
        )

    class Meta:
        model = GenderResponse
        fields = ['value']
