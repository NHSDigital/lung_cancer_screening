from django import forms

from ...nhsuk_forms.choice_field import ChoiceField
from ..models.education_response import EducationResponse, EducationValues


class EducationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = ChoiceField(
            choices=EducationValues.choices,
            label="What level of education have you completed?",
            widget=forms.RadioSelect,
            label_classes="nhsuk-fieldset__legend--l",
            label_is_page_heading=True,
            hint=(
                "Select all that apply"
            ),
            error_messages={
                'required': 'Select your level of education'
            }
        )

        self["value"].add_divider_after(
            EducationValues.POSTGRADUATE_DEGREE.value, "or"
        )

    class Meta:
        model = EducationResponse
        fields = ['value']
