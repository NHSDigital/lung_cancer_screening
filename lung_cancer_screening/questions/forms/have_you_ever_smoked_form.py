from django import forms

from ...nhsuk_forms.typed_choice_field import TypedChoiceField
from ..models.response_set import ResponseSet, HaveYouEverSmokedValues

class HaveYouEverSmokedForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["have_you_ever_smoked"] = TypedChoiceField(
            choices=HaveYouEverSmokedValues.choices,
            widget=forms.RadioSelect,
            label="Have you ever smoked?",
            label_classes="nhsuk-fieldset__legend--m",
            hint="This includes social smoking",
            coerce=int,
            error_messages={
                'required': 'Select if you have ever smoked'
            }
        )

    class Meta:
        model = ResponseSet
        fields = ['have_you_ever_smoked']
