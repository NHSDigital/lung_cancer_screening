from django import forms

from ...nhsuk_forms.typed_choice_field import TypedChoiceField
from ..models.response_set import ResponseSet, SexAtBirthValues

class SexAtBirthForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.participant = kwargs.pop('participant')
        super().__init__(*args, **kwargs)
        self.instance.participant = self.participant

        self.fields["sex_at_birth"] = TypedChoiceField(
            choices=SexAtBirthValues.choices,
            widget=forms.RadioSelect,
            label="What was your sex at birth?",
            label_classes="nhsuk-fieldset__legend--m",
            hint="Your sex may impact your chances of developing lung cancer.",
            error_messages={
                'required': 'Select your sex at birth.'
            }
        )

    class Meta:
        model = ResponseSet
        fields = ['sex_at_birth']
