from django import forms
from ...nhsuk_forms.choice_field import ChoiceField
from ..models.response_set import ResponseSet, AsbestosExposureValues


class AsbestosExposureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.participant = kwargs.pop('participant')
        super().__init__(*args, **kwargs)
        self.instance.participant = self.participant

        self.fields["asbestos_exposure"] = ChoiceField(
            choices=AsbestosExposureValues.choices,
            widget=forms.RadioSelect,
            label="Have you ever worked in a job where you might have been exposed to asbestos?",
            label_classes="nhsuk-fieldset__legend--m",
            error_messages={
                'required': 'Select if you have been exposed to asbestos.'
            }
        )

    class Meta:
        model = ResponseSet
        fields = ['asbestos_exposure']
