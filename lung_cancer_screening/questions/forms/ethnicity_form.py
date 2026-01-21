from django import forms

from ...nhsuk_forms.choice_field import ChoiceField
from ..models.ethnicity_response import EthnicityResponse, EthnicityValues


class EthnicityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = ChoiceField(
            choices=EthnicityValues.choices,
            label="What is your ethnic background?",
            widget=forms.RadioSelect,
            label_classes="nhsuk-fieldset__legend--m",
            error_messages={
                'required': 'Select your ethnic background'
            }
        )

        self["value"].add_divider_after(
            EthnicityValues.OTHER.value, "or"
        )

    class Meta:
        model = EthnicityResponse
        fields = ['value']
