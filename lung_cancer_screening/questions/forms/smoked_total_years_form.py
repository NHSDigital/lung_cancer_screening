from django import forms

from ...nhsuk_forms.integer_field import IntegerField
from ..models.smoked_total_years_response import SmokedTotalYearsResponse


class SmokedTotalYearsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = IntegerField(
            label="Roughly how many years have you smoked cigarettes?",
            label_is_page_heading=True,
            label_classes="nhsuk-label--l",
            classes="nhsuk-input--width-4",
            hint="Give an estimate if you are not sure",
            required=True,
            suffix="years",
            error_messages={
                "required": "Enter the number of years you have smoked cigarettes",
                "invalid": "Years must be in whole numbers"
            },
        )

    class Meta:
        model = SmokedTotalYearsResponse
        fields = ['value']
