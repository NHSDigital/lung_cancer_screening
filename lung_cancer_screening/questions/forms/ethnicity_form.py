from django import forms

from ...nhsuk_forms.choice_field import ChoiceField
from ..models.response_set import ResponseSet, EthnicityValues

class EthnicityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.participant = kwargs.pop('participant')
        super().__init__(*args, **kwargs)
        self.instance.participant = self.participant

        self.fields["ethnicity"] = ChoiceField(
            choices=EthnicityValues.choices,
            label="What is your ethnic background?",
            widget=forms.RadioSelect,
            label_classes="nhsuk-fieldset__legend--m",
            label_is_page_heading=True,
            hint="Your ethnicity may impact your chances of developing lung cancer.",
            error_messages={
                'required': 'Select your ethnic background'
            }
        )

        self["ethnicity"].add_divider_after(EthnicityValues.OTHER.value, "or")

    class Meta:
        model = ResponseSet
        fields = ['ethnicity']
