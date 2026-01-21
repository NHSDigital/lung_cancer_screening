from django import forms
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
                'required': 'Enter your age when you started smoking',
                'invalid': 'Enter your age when you started smoking',
                'zero_entered':'The age you started smoking must be between 1 and your current age',
                'old_current_age':'The age you started smoking must be the same as, or younger than your current age'
            }
        )

    class Meta:
        model = AgeWhenStartedSmokingResponse
        fields = ['value']
