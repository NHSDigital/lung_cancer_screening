from django import forms
from django.urls import reverse_lazy
from django.utils.html import format_html

from lung_cancer_screening.nhsuk_forms.integer_field import IntegerField
from ..models.when_you_quit_smoking_response import WhenYouQuitSmokingResponse

class WhenYouQuitSmokingForm(forms.ModelForm):
    class Meta:
        model = WhenYouQuitSmokingResponse
        fields = ["value"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = IntegerField(
            label="How old were you when you quit smoking?",
            label_classes="nhsuk-label--m",
            classes="nhsuk-input--width-2",
            hint="Give an estimate if you are not sure",
            prefix="Age",
            error_messages={
                "required": "Enter your age when you quit smoking",
                "invalid": "Enter your age when you quit smoking",
                "min_value":"The age you quit smoking must be between 1 and your current age",
                "age_when_quit_smoking_greater_than_age_started":"The age you quit smoking cannot be lower than the age you started smoking",
                "no_date_of_birth" : format_html("<a href=\"{}\">Provide your date of birth</a> before answering this question", reverse_lazy("questions:date_of_birth"))
            }
        )
