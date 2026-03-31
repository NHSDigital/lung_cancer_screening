from django import forms

from ...nhsuk_forms.integer_field import IntegerField
from ...nhsuk_forms.typed_choice_field import TypedChoiceField
from ..models.periods_when_you_stopped_smoking_response import PeriodsWhenYouStoppedSmokingResponse


class PeriodsWhenYouStoppedSmokingForm(forms.ModelForm):
    class Meta:
        model = PeriodsWhenYouStoppedSmokingResponse
        fields = ["value", "duration_years"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk and self.instance.value is not None:
            self.initial["value"] = "True" if self.instance.value else "False"

        self.fields["value"] = TypedChoiceField(
            choices=[("True", "Yes"), ("False", "No")],
            widget=forms.RadioSelect,
            label=self.label(),
            label_is_page_heading=not self.response_set().current_smoker(),
            label_classes=self.label_classes(),

            coerce=lambda x: x == "True",
            error_messages={
                "required": self.required_error_message()
            },
        )

        self.fields["duration_years"] = IntegerField(
            label=self.duration_years_label(),
            label_classes="nhsuk-fieldset__legend--s",
            classes="nhsuk-input--width-4",
            hint=self.duration_years_hint(),
            required=False,
            suffix="years",
        )

    def clean_duration_years(self):
        value = self.cleaned_data.get("value")
        duration_years = self.cleaned_data.get("duration_years")

        if value is False:
            return None

        if duration_years is None:
            raise forms.ValidationError(self.duration_years_required_error_message())

        return duration_years


    def response_set(self):
        return self.instance.response_set


    def label(self):
        if self.response_set().current_smoker():
            return "Have you ever stopped smoking for periods of 1 year or longer?"
        else:
            return "Did you ever stop or quit smoking for periods of 1 year or longer?"


    def label_is_page_heading(self):
        return not self.response_set().current_smoker()


    def label_classes(self):
        if self.label_is_page_heading():
            return "nhsuk-fieldset__legend--l"
        else:
            return "nhsuk-fieldset__legend--m"

    def page_title(self):
        return f"{self.label()} – NHS"


    def stopped_or_quit(self):
        if self.response_set().current_smoker():
            return "stopped "
        else:
            return "stopped or quit "


    def required_error_message(self):
        return f"Select if you ever {self.stopped_or_quit()}smoking for periods of 1 year or longer"


    def duration_years_required_error_message(self):
        return f"Enter the total number of years you {self.stopped_or_quit()}smoking"


    def duration_years_label(self):
        if self.response_set().current_smoker():
            return "Enter the total number of years you stopped smoking"
        else:
            return "Roughly how many years did you stop or quit smoking in total?"


    def duration_years_hint(self):
        if self.response_set().current_smoker():
            return "Give an estimate if you are not sure"
        else:
            return "Add together the periods when you stopped smoking and the number of years since you quit. Give an estimate if you are not sure."
