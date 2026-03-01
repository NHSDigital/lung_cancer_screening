from django import forms


from ..models.smoking_frequency_response import SmokingFrequencyResponse, SmokingFrequencyValues

from ...nhsuk_forms.typed_choice_field import TypedChoiceField

class SmokingFrequencyForm(forms.ModelForm):
    def __init__(self, *args, tobacco_smoking_history_item, normal_tobacco_smoking_history_item = None, **kwargs):
        super().__init__(*args, **kwargs)

        self.tobacco_smoking_history_item = tobacco_smoking_history_item
        self.normal_tobacco_smoking_history_item = normal_tobacco_smoking_history_item

        self.fields["value"] = TypedChoiceField(
            choices=SmokingFrequencyValues.choices,
            widget=forms.RadioSelect,
            label=self._get_label_for_value(),
            label_classes="nhsuk-fieldset__legend--l",
            label_is_page_heading=True,
            error_messages={
                'required': 'Select how often you smoke cigarettes',
            }
        )

        value_field = self["value"]
        value_field.add_hint_for_choice(
            SmokingFrequencyValues.WEEKLY,
            "For example, on the weekend"
        )
        value_field.add_hint_for_choice(
            SmokingFrequencyValues.MONTHLY,
            "Select this option if you smoke once a month, or once every few months",
        )

    class Meta:
        model = SmokingFrequencyResponse
        fields = ['value']

    def more_or_fewer_string(self):
        return "more" if self.tobacco_smoking_history_item.is_increased() else "fewer"

    def amount_prefix(self):
        return "grams of " if self.tobacco_smoking_history_item.is_rolling_tobacco() else ""

    def _get_label_for_value(self):
        if self.tobacco_smoking_history_item.is_normal():
            return f"How often do you smoke {self.tobacco_smoking_history_item.human_type().lower()}?"

        return f"When you smoked {self.more_or_fewer_string()} than {self.__get_smoking_string()}, how often did you smoke {self.tobacco_smoking_history_item.human_type().lower()}?"

    def __get_smoking_string(self):
        amount = self.normal_tobacco_smoking_history_item.amount()
        frequency = self.normal_tobacco_smoking_history_item.frequency_singular()
        return f"{amount} {self.amount_prefix()}{self.tobacco_smoking_history_item.human_type().lower()} a {frequency}"
