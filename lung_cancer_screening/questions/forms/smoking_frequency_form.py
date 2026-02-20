from django import forms

from lung_cancer_screening.questions.models.tobacco_smoking_history import TobaccoSmokingHistory

from ..models.smoking_frequency_response import SmokingFrequencyResponse, SmokingFrequencyValues

from ...nhsuk_forms.typed_choice_field import TypedChoiceField

class SmokingFrequencyForm(forms.ModelForm):
    def __init__(self, *args, response_set, tobacco_smoking_history_item, **kwargs):
        super().__init__(*args, **kwargs)

        self.response_set = response_set
        self.tobacco_smoking_history_item = tobacco_smoking_history_item

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

    def _get_label_for_value(self):
        if self.tobacco_smoking_history_item.level == TobaccoSmokingHistory.Levels.DECREASED:
            return f"When you smoked fewer than {self.__get_smoking_string()}, how often did you smoke {self.tobacco_smoking_history_item.human_type().lower()}?"
        if self.tobacco_smoking_history_item.level == TobaccoSmokingHistory.Levels.INCREASED:
            return f"When you smoked more than {self.__get_smoking_string()}, how often did you smoke {self.tobacco_smoking_history_item.human_type().lower()}?"
        return f"How often do you smoke {self.tobacco_smoking_history_item.human_type().lower()}?"

    def __get_smoking_string(self):
        normal_smoking_history_for_type = self.response_set.tobacco_smoking_history.filter(level=TobaccoSmokingHistory.Levels.NORMAL).first()
        amount = normal_smoking_history_for_type.smoked_amount_response.value
        frequency = normal_smoking_history_for_type.smoking_frequency_response.get_value_display_as_singleton_text()
        return f"{amount} {self.tobacco_smoking_history_item.human_type().lower()} a {frequency}"
