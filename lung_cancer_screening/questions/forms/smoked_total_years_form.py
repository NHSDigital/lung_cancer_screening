from django import forms

from ...nhsuk_forms.integer_field import IntegerField
from ..models.smoked_total_years_response import SmokedTotalYearsResponse
from .mixins.smoking_form_presenter import SmokingFormPresenter


class SmokedTotalYearsForm(SmokingFormPresenter, forms.ModelForm):
    def __init__(self, tobacco_smoking_history, *args, **kwargs):
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
                "max_value": self.greater_than_years_smoked_error_message()
            },
        )


    def normal_label(self):
        return (
            f"Roughly how many years {self.presenter.have_you_smoked_or_did_you_smoke()} "
            f"{self.presenter.human_type().lower()}?"
        )


    def changed_label(self):
        return (
            f"Roughly how many years did you smoke {self.presenter.to_sentence()}?"
        )


    def label(self):
        if self.tobacco_smoking_history.is_normal():
            return self.normal_label()
        else:
            return self.changed_label()


    def normal_required_error_message(self):
        have_text = "have " if self.presenter.is_present_tense() else ""
        return (
            f"Enter the number of years you {have_text}smoked "
            f"{self.presenter.human_type().lower()}"
        )


    def changed_required_error_message(self):
        return (
            "Enter the number of years you smoked "
            f"{self.presenter.to_sentence()}"
        )


    def required_error_message(self):
        if self.tobacco_smoking_history.is_normal():
            return self.normal_required_error_message()
        else:
            return self.changed_required_error_message()


    def normal_min_value_error_message(self):
        return (
            "The number of years you smoked "
            f"{self.presenter.human_type().lower()} must be at least 1"
        )


    def changed_min_value_error_message(self):
        return (
            "The number of years you smoked "
            f"{self.presenter.to_sentence()} must be at least 1"
        )


    def min_value_error_message(self):
        if self.tobacco_smoking_history.is_normal():
            return self.normal_min_value_error_message()
        else:
            return self.changed_min_value_error_message()


    def normal_greater_than_years_smoked_error_message(self):
        return (
            f"The number of years you smoked {self.presenter.human_type().lower()} "
            "must be equal to, or fewer than, the total number of years you smoked"
        )


    def changed_greater_than_years_smoked_error_message(self):
        return (
            f"The number of years you smoked {self.presenter.to_sentence()} "
            "must be equal to, or fewer than, the total number of years you have been smoking"
        )


    def greater_than_years_smoked_error_message(self):
        if self.tobacco_smoking_history.is_normal():
            return self.normal_greater_than_years_smoked_error_message()
        else:
            return self.changed_greater_than_years_smoked_error_message()


    def page_title(self):
        if self.tobacco_smoking_history.is_normal():
            smoked_text = "have smoked" if self.presenter.is_present_tense() else "smoked"
            return f"Number of years you {smoked_text} {self.presenter.human_type().lower()} - NHS"
        if self.tobacco_smoking_history.is_increased() or self.tobacco_smoking_history.is_decreased():
            return f"Number of years you smoked {self.presenter.human_type().lower()} when your smoking {self.presenter.increased_or_decreased()} - NHS"
        else:
            return f"Number of years you smoked {self.presenter.human_type().lower()} - NHS"


    class Meta:
        model = SmokedTotalYearsResponse
        fields = ['value']
