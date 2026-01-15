from django import forms

from ...nhsuk_forms.choice_field import MultipleChoiceField
from ..models.education_response import EducationResponse, EducationValues


class EducationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = MultipleChoiceField(
            choices=EducationValues.choices,
            label="What level of education have you completed?",
            widget=forms.CheckboxSelectMultiple,
            label_classes="nhsuk-fieldset__legend--m",
            hint="Select all that apply",
            error_messages={
                "required": "Select your level of education",
                "singleton_option": (
                    "Select your level of education, or select "
                    "'Prefer not to say'"
                ),
            },
        )

        self["value"].add_divider_after(
            EducationValues.POSTGRADUATE_DEGREE.value, "or"
        )

    class Meta:
        model = EducationResponse
        fields = ['value']
