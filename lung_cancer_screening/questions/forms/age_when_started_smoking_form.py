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


    def save(self, commit=True):
        instance = super(AgeWhenStartedSmokingForm, self).save(commit=False)

        self._cleanup_periods_stopped_smoking_if_value_changed()

        if commit:
            instance.save()

        return instance

    def _cleanup_periods_stopped_smoking_if_value_changed(self):
        if 'value' in self.changed_data and hasattr(self.instance.response_set, 'periods_when_you_stopped_smoking_response'):
            self.instance.response_set.periods_when_you_stopped_smoking_response.delete()
