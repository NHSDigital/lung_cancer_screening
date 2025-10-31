from django import forms

from ...nhsuk_forms.typed_choice_field import TypedChoiceField
from ..models.response_set import ResponseSet, GenderValues

class GenderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.participant = kwargs.pop('participant')
        super().__init__(*args, **kwargs)
        self.instance.participant = self.participant

        self.fields["gender"] = TypedChoiceField(
            choices=GenderValues.choices,
            widget=forms.RadioSelect,
            label="Which of these best describes you?",
            label_classes="nhsuk-fieldset__legend--m",
            hint="This information is used to find your NHS number and match with your GP record.",
            error_messages={
                'required': 'Select the option that best describes your gender.'
            }
        )

    class Meta:
        model = ResponseSet
        fields = ['gender']
