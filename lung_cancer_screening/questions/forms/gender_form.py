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
            label_classes="nhsuk-fieldset__legend--l",
            label_is_page_heading=True,
            hint=(
                "This information is used to find your NHS number and "
                "match with your GP record."
            ),
            error_messages={
                'required': 'Select the option that best describes your gender'
            }
        )

    class Meta:
        model = GenderResponse
        fields = ['value']
