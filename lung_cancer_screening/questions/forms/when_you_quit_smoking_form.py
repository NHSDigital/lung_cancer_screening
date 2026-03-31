from django import forms

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
                # "age_started_smoking_greater_than_current_age":"The age you started smoking must be the same as, or less than your current age",
                # "no_date_of_birth" : format_html("<a href=\"{}\">Provide your date of birth</a> before answering this question", reverse_lazy("questions:date_of_birth"))
            }
        )
