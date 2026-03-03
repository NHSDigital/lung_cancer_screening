from django import forms

from ...nhsuk_forms.integer_field import IntegerField
from ..models.smoked_amount_response import SmokedAmountResponse


class SmokedAmountForm(forms.ModelForm):

    def __init__(self, tobacco_smoking_history, normal_tobacco_smoking_history = None, *args, **kwargs):
        self.tobacco_smoking_history = tobacco_smoking_history
        self.normal_tobacco_smoking_history = normal_tobacco_smoking_history

        super().__init__(*args, **kwargs)

        self.fields["value"] = IntegerField(
            label=self._type_label(),
            label_classes="nhsuk-label--m" if self.tobacco_smoking_history.is_normal() else "nhsuk-label--l",
            label_is_page_heading=not self.tobacco_smoking_history.is_normal(),
            classes="nhsuk-input--width-4",
            hint="Give an estimate if you are not sure",
            suffix=self.type_string(),
            required=True,
            error_messages={
                "required": self._type_required_error_message(),
                "min_value": self._type_min_value_error_message()
            },
        )

    def type_string(self):
        return self.tobacco_smoking_history.human_type().lower()


    def more_or_fewer_text(self):
        if self.tobacco_smoking_history.is_increased():
            return "more"
        elif self.tobacco_smoking_history.is_decreased():
            return "fewer"


    def _normal_type_label(self):
        do_or_did = "do" if self.tobacco_smoking_history.is_current() else "did"
        return (
            f"Roughly how many {self.type_string()} {do_or_did} you "
            f"{self._currently_or_previously_text()} smoke in a normal "
            f"{self.tobacco_smoking_history.frequency_singular()}?"
        )


    def _changed_type_label(self):
        return f"When you smoked {self.more_or_fewer_text()} than {self.normal_tobacco_smoking_history.amount()} {self.type_string()} a {self.normal_tobacco_smoking_history.frequency_singular()}, roughly how many {self.type_string()} did you normally smoke a {self.tobacco_smoking_history.frequency_singular()}?"


    def _type_label(self):
        if self.normal_tobacco_smoking_history:
            return self._changed_type_label()
        else:
            return self._normal_type_label()


    def _currently_or_previously_text(self):
        return "currently" if self.tobacco_smoking_history.is_current() else "previously"


    def _normal_type_required_error_message(self):
        return (
            f"Enter how many {self.type_string()} you "
            f"{self._currently_or_previously_text()} {self.smoke_or_smoked_text()} "
            f"in a normal {self.tobacco_smoking_history.frequency_singular()}"
        )


    def _changed_type_required_error_message(self):
        return f"Enter the number of {self.type_string()} you smoked when you smoked {self.more_or_fewer_text()} than {self.normal_tobacco_smoking_history.amount()} {self.type_string()} a {self.normal_tobacco_smoking_history.frequency_singular()}"


    def _type_required_error_message(self):
        if self.normal_tobacco_smoking_history:
            return self._changed_type_required_error_message()
        else:
            return self._normal_type_required_error_message()

    def smoke_or_smoked_text(self):
        if self.tobacco_smoking_history.is_current():
            return "smoke"
        else:
            return "smoked"


    def _type_min_value_error_message(self):
        return (
            f"The number of {self.type_string()} you {self.smoke_or_smoked_text()} "
            f"a {self.tobacco_smoking_history.frequency_singular()} "
            "must be at least 1"
        )

    class Meta:
        model = SmokedAmountResponse
        fields = ['value']
