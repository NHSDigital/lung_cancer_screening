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
                "required": self.required_error_message(),
                "invalid": "Years must be in whole numbers"
            },
        )

    def normal_label(self):
        return (
            f"Roughly how many years have you smoked "
            f"{self.tobacco_smoking_history.human_type().lower()}?"
        )

    def changed_label(self):
        return (
            f"Roughly how many years did you smoke {self.tobacco_smoking_history.amount()} "
            f"{self.tobacco_smoking_history.unit()} "
            f"a {self.tobacco_smoking_history.frequency_singular()}?"
        )

    def label(self):
        if self.tobacco_smoking_history.is_normal():
            return self.normal_label()
        else:
            return self.changed_label()

    def normal_required_error_message(self):
        return (
            "Enter the number of years you have smoked "
            f"{self.tobacco_smoking_history.human_type().lower()}"
        )

    def changed_required_error_message(self):
        return (
            "Enter the number of years you have smoked "
            f"{self.tobacco_smoking_history.amount()} "
            f"{self.tobacco_smoking_history.unit()} "
            f"a {self.tobacco_smoking_history.frequency_singular()}"
        )

    def required_error_message(self):
        if self.tobacco_smoking_history.is_normal():
            return self.normal_required_error_message()
        else:
            return self.changed_required_error_message()

    class Meta:
        model = SmokedTotalYearsResponse
        fields = ['value']
