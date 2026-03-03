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
                "invalid": "Years must be in whole numbers",
                "min_value": self.min_value_error_message(),
            },
        )


    def normal_required_error_message(self):
        return (
            "Enter the number of years you have smoked "
            f"{self.tobacco_smoking_history.human_type().lower()}"
        )

    def changed_required_error_message(self):
        return (
            "Enter the number of years you smoked "
            f"{self.tobacco_smoking_history.to_sentence()}"
        )

    def required_error_message(self):
        if self.tobacco_smoking_history.is_normal():
            return self.normal_required_error_message()

        return self.changed_required_error_message()


    def normal_min_value_error_message(self):
        return (
            "The number of years you smoked "
            f"{self.tobacco_smoking_history.human_type().lower()} "
            "must be at least 1"
        )


    def changed_min_value_error_message(self):
        return (
            "The number of years you smoked "
            f"{self.tobacco_smoking_history.to_sentence()} "
            "must be at least 1"
        )


    def min_value_error_message(self):
        if self.tobacco_smoking_history.is_normal():
            return self.normal_min_value_error_message()

        return self.changed_min_value_error_message()


    def normal_label(self):
        return f"Roughly how many years have you smoked {self.tobacco_smoking_history.human_type().lower()}?"

    def changed_label(self):
        return f"Roughly how many years did you smoke {self.tobacco_smoking_history.to_sentence()}?"

    def label(self):
        if self.tobacco_smoking_history.is_normal():
            return self.normal_label()

        return self.changed_label()

    class Meta:
        model = SmokedTotalYearsResponse
        fields = ['value']
