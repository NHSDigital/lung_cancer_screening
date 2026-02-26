from django import forms

from ...nhsuk_forms.integer_field import IntegerField
from ..models.smoked_total_years_response import SmokedTotalYearsResponse


class SmokedTotalYearsForm(forms.ModelForm):

    def __init__(self, tobacco_smoking_history,*args, **kwargs):
        self.tobacco_smoking_history = tobacco_smoking_history
        super().__init__(*args, **kwargs)

        self.fields["value"] = IntegerField(
            label=self.label(),
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

    def label(self):
        if self.tobacco_smoking_history.is_normal():
            return f"Roughly how many years have you smoked {self.tobacco_smoking_history.human_type().lower()}?"
        else:
            return f"Roughly how many years did you smoke {self.tobacco_smoking_history.amount()} {self.tobacco_smoking_history.human_type().lower()} a {self.tobacco_smoking_history.frequency_singular()}?"

    class Meta:
        model = SmokedTotalYearsResponse
        fields = ['value']
