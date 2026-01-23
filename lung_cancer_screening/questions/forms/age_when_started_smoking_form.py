from django import forms
from django.urls import reverse_lazy
from django.utils.html import format_html

from ...nhsuk_forms.integer_field import IntegerField
from ..models.age_when_started_smoking_response import AgeWhenStartedSmokingResponse

class AgeWhenStartedSmokingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = IntegerField(
            label="How old were you when you started smoking?",
            label_classes="nhsuk-fieldset__legend--l",
            label_is_page_heading=True,
            classes="nhsuk-input--width-2",
            hint="Give an estimate if you are not sure",
            prefix="Age",
            error_messages={
                "required": "Enter your age when you started smoking",
                "invalid": "Enter your age when you started smoking",
                "zero_entered":"The age you started smoking must be between 1 and your current age",
                "age_started_smoking_greater_than_current_age":"The age you started smoking must be the same as, or less than your current age",
                "no_date_of_birth" : format_html("<a href=\"{}\">Provide your date of birth</a> before answering this question", reverse_lazy("questions:date_of_birth"))
            }
        )

    class Meta:
        model = AgeWhenStartedSmokingResponse
        fields = ["value"]
