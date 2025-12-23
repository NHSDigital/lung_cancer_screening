from django import forms

from ...nhsuk_forms.choice_field import ChoiceField
from ..models.sex_at_birth_response import SexAtBirthResponse, SexAtBirthValues


class SexAtBirthForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = ChoiceField(
            choices=SexAtBirthValues.choices,
            widget=forms.RadioSelect,
            label="What was your sex at birth?",
            label_classes="nhsuk-fieldset__legend--l",
            label_is_page_heading=True,
            hint=(
                "Your sex may impact your chances of developing lung cancer."
            ),
            error_messages={
                'required': 'Select your sex at birth'
            }
        )

    class Meta:
        model = SexAtBirthResponse
        fields = ['value']
