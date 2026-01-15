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

        # Add hints for each choice
        education_field = self["value"]
        education_field.add_hint_for_choice(
            EducationValues.GCSES,
            "Previously O-levels",
        )
        education_field.add_hint_for_choice(
            EducationValues.A_LEVELS,
            "Previously Higher School Certificate (HSC)",
        )
        education_field.add_hint_for_choice(
            EducationValues.BACHELORS_DEGREE,
            "A university degree, also known as an undergraduate degree",
        )
        education_field.add_hint_for_choice(
            EducationValues.POSTGRADUATE_DEGREE,
            "For example, a Masters or PhD",
        )

        self["value"].add_divider_after(
            EducationValues.POSTGRADUATE_DEGREE.value, "or"
        )

    class Meta:
        model = EducationResponse
        fields = ['value']
