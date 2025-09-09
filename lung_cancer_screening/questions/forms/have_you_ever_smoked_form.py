from django import forms

from lung_cancer_screening.core.form_fields import TypedChoiceField
from ..models.response_set import ResponseSet, HaveYouEverSmokedValues

class HaveYouEverSmokedForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.participant = kwargs.pop('participant')
        super().__init__(*args, **kwargs)
        self.instance.participant = self.participant

        self.fields["have_you_ever_smoked"] = TypedChoiceField(
            choices=HaveYouEverSmokedValues.choices,
            widget=forms.RadioSelect,
            label="Have you ever smoked?",
            label_classes="nhsuk-fieldset__legend--m",
            coerce=int
        )

    class Meta:
        model = ResponseSet
        fields = ['have_you_ever_smoked']
