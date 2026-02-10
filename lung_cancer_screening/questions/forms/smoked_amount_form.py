from django import forms

from ...nhsuk_forms.integer_field import IntegerField
from ..models.smoked_amount_response import SmokedAmountResponse


class SmokedAmountForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.frequency_text = kwargs.pop("frequency_text", "day")

        super().__init__(*args, **kwargs)

        self.fields["value"] = IntegerField(
            label=self._type_label(),
            label_classes="nhsuk-label--m",
            classes="nhsuk-input--width-4",
            hint="Give an estimate if you are not sure",
            suffix=self._type_suffix(),
            required=True,
            error_messages={
                "required": self._type_required_error_message(),
                "min_value": self._type_min_value_error_message()
            },
        )

    def type_string(self):
        return self.instance.tobacco_smoking_history.human_type().lower()

    def _type_label(self):
        return f"Roughly how many {self.type_string()} do you smoke in a normal {self.frequency_text}?"

    def _type_required_error_message(self):
        return f"Enter how many {self.type_string()} you currently smoke in a normal {self.frequency_text}"

    def _type_min_value_error_message(self):
        return f"The number of {self.type_string()} you smoke must be at least 1"

    def _type_suffix(self):
        return self.type_string()

    class Meta:
        model = SmokedAmountResponse
        fields = ['value']
