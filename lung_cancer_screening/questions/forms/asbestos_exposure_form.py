from django import forms
from ...nhsuk_forms.typed_choice_field import TypedChoiceField
from ..models.response_set import ResponseSet


class AsbestosExposureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.participant = kwargs.pop('participant')
        super().__init__(*args, **kwargs)
        self.instance.participant = self.participant

        self.fields["asbestos_exposure"] = TypedChoiceField(
            choices=[(True, 'Yes'), (False, 'No')],
            widget=forms.RadioSelect,
            label="Have you ever worked in a job where you might have been exposed to asbestos?",
            label_classes="nhsuk-fieldset__legend--l",
            coerce=lambda x: x == 'True',
            error_messages={
                'required': 'Select if you have been exposed to asbestos'
            }
        )

    class Meta:
        model = ResponseSet
        fields = ['asbestos_exposure']
