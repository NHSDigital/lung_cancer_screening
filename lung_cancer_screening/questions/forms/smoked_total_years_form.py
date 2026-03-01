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

    def amount_prefix(self):
        return "grams of " if self.tobacco_smoking_history.is_rolling_tobacco() else ""

    def normal_label(self):
        return (
            f"Roughly how many years have you smoked "
            f"{self.tobacco_smoking_history.human_type().lower()}?"
        )

    def changed_label(self):
        return (
            f"Roughly how many years did you smoke {self.tobacco_smoking_history.amount()} "
            f"{self.amount_prefix()}{self.tobacco_smoking_history.human_type().lower()} "
            f"a {self.tobacco_smoking_history.frequency_singular()}?"
        )

    def label(self):
        if self.tobacco_smoking_history.is_normal():
            return self.normal_label()
        else:
            return self.changed_label()

    class Meta:
        model = SmokedTotalYearsResponse
        fields = ['value']
