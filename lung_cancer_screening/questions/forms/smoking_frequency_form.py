from django import forms


from ..models.smoking_frequency_response import SmokingFrequencyResponse, SmokingFrequencyValues

from ...nhsuk_forms.typed_choice_field import TypedChoiceField
from .mixins.smoking_form_presenter import SmokingFormPresenter

class SmokingFrequencyForm(SmokingFormPresenter, forms.ModelForm):
    def __init__(self, *args, tobacco_smoking_history, normal_tobacco_smoking_history = None, **kwargs):
        super().__init__(*args, **kwargs)

        self.response_set = tobacco_smoking_history.response_set
        self.tobacco_smoking_history = tobacco_smoking_history
        self.normal_tobacco_smoking_history = normal_tobacco_smoking_history

        self.fields["value"] = TypedChoiceField(
            choices=SmokingFrequencyValues.choices,
            widget=forms.RadioSelect,
            label=self.label(),
            label_classes="nhsuk-fieldset__legend--l",
            label_is_page_heading=True,
            error_messages={
                'required': self.required_error_message(),
            }
        )

        value_field = self["value"]
        value_field.add_hint_for_choice(
            SmokingFrequencyValues.WEEKLY,
            "For example, on the weekend"
        )
        smoke_or_smoked = "smoke" if self.response_set.current_smoker() else "smoked"
        value_field.add_hint_for_choice(
            SmokingFrequencyValues.MONTHLY,
            f"Select this option if you {smoke_or_smoked} at least once a month",
        )
        value_field.add_hint_for_choice(
            SmokingFrequencyValues.YEARLY,
            "For example, 2 to 3 times a year or fewer",
        )

    class Meta:
        model = SmokingFrequencyResponse
        fields = ['value']


    def normal_label(self):
        return (
            f"How often {self.presenter.do_or_did()} "
            f"you smoke {self.presenter.human_type().lower()}?"
        )


    def changed_label(self):
        return (
            f"When you smoked {self.presenter.more_or_fewer()} "
            f"than {self.normal_presenter.to_sentence()}, how often did "
            f"you smoke {self.presenter.human_type().lower()}?"
        )


    def label(self):
        if self.tobacco_smoking_history.is_normal():
            return self.normal_label()
        else:
            return self.changed_label()


    def normal_required_error_message(self):
        return (
            f"Select how often you {self.presenter.smoke_or_smoked()} "
            f"{self.presenter.human_type().lower()}"
        )


    def changed_required_error_message(self):
        return (
            f"Select how often you smoked {self.presenter.human_type().lower()} "
            f"when you smoked {self.presenter.more_or_fewer()} "
            f"than {self.normal_presenter.to_sentence()}"
        )


    def required_error_message(self):
        if self.tobacco_smoking_history.is_normal():
            return self.normal_required_error_message()
        else:
            return self.changed_required_error_message()


    def page_title(self):
        if self.tobacco_smoking_history.is_normal():
            return(f"How often {self.presenter.do_or_did()} you smoke {self.presenter.human_type().lower()}?")
        else:
            return f"How often you {self.presenter.smoke_or_smoked()} {self.presenter.human_type().lower()} when your smoking {self.presenter.increased_or_decreased()}"
