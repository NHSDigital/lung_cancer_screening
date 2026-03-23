from django import forms

from ...nhsuk_forms.integer_field import IntegerField
from ..models.smoked_amount_response import SmokedAmountResponse

from .mixins.smoking_form_presenter import SmokingFormPresenter


class SmokedAmountForm(SmokingFormPresenter, forms.ModelForm):

    def __init__(self, tobacco_smoking_history, normal_tobacco_smoking_history = None, *args, **kwargs):
        self.tobacco_smoking_history = tobacco_smoking_history
        self.normal_tobacco_smoking_history = normal_tobacco_smoking_history

        super().__init__(*args, **kwargs)

        self.fields["value"] = IntegerField(
            label=self.label(),
            label_classes="nhsuk-label--m" if self.tobacco_smoking_history.is_normal() else "nhsuk-label--l",
            label_is_page_heading=not self.tobacco_smoking_history.is_normal(),
            classes="nhsuk-input--width-4",
            hint="Give an estimate if you are not sure",
            suffix=self.suffix(),
            required=True,
            error_messages={
                "required": self.required_error_message(),
                "min_value": self.min_value_error_message()
            },
        )


    def suffix(self):
        return "grams" if self.tobacco_smoking_history.is_rolling_tobacco() else self.presenter.unit()


    def normal_label(self):
        is_current = self.tobacco_smoking_history.is_current()
        middle = "currently smoke in a normal " if is_current else "normally smoke a "
        return (
            f"Roughly how many {self.presenter.unit()} "
            f"{self.presenter.do_or_did()} you {middle}"
            f"{self.presenter.frequency()}?"
        )


    def changed_label(self):
        return (
            f"When you smoked {self.presenter.more_or_fewer()} than "
            f"{self.normal_presenter.to_sentence()}, "
            f"roughly how many {self.presenter.unit()} "
            f"did you normally smoke a {self.presenter.frequency()}?"
        )


    def label(self):
        if self.tobacco_smoking_history.is_normal():
            return self.normal_label()
        else:
            return self.changed_label()


    def normal_required_error_message(self):
        return (
            f"Enter how many {self.presenter.unit()} you "
            f"{self.presenter.currently_or_previously()} {self.presenter.smoke_or_smoked()} "
            f"in a normal {self.presenter.frequency()}"
        )

    def changed_required_error_message(self):
        return (
            f"Enter the number of {self.presenter.unit()} "
            f"you smoked when you smoked {self.presenter.more_or_fewer()} than "
            f"{self.normal_presenter.to_sentence()}"
        )


    def required_error_message(self):
        if self.normal_tobacco_smoking_history:
            return self.changed_required_error_message()
        else:
            return self.normal_required_error_message()


    def min_value_error_message(self):
        return (
            f"The number of {self.presenter.unit()} you "
            f"{self.presenter.smoke_or_smoked()} a {self.presenter.frequency()} "
            "must be at least 1"
        )

    def page_title(self) -> str:
        if self.tobacco_smoking_history.is_normal():
            return (f"Number of {self.presenter.unit()} you normally {self.presenter.smoke_or_smoked()}")
        else:
            return(f"Number of {self.presenter.unit()} you smoked when your smoking {self.presenter.increased_or_decreased()}")

    class Meta:
        model = SmokedAmountResponse
        fields = ['value']
