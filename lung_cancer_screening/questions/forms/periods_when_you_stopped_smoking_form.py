from django import forms

from ...nhsuk_forms.integer_field import IntegerField
from ...nhsuk_forms.typed_choice_field import TypedChoiceField
from ..models.periods_when_you_stopped_smoking_response import PeriodsWhenYouStoppedSmokingResponse


class PeriodsWhenYouStoppedSmokingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = TypedChoiceField(
            choices=[(True, "Yes"), (False, "No")],
            widget=forms.RadioSelect,
            label="Have you ever stopped smoking for periods of 1 year or longer?",
            label_classes="nhsuk-fieldset__legend--m",
            coerce=lambda x: x == "True",
            error_messages={
                "required": "Select if you ever stopped smoking for periods of 1 year or longer"
            },
        )

        self.fields["duration_years"] = IntegerField(
            label="Enter the total number of years you stopped smoking for",
            label_classes="nhsuk-fieldset__legend--s",
            classes="nhsuk-input--width-4",
            hint="Give an estimate if you are not sure",
            required=False,
            suffix="years",
            error_messages={
                "required": "Enter the total number of years you stopped smoking for"
            },
        )

    class Meta:
        model = PeriodsWhenYouStoppedSmokingResponse
        fields = ["value", "duration_years"]
