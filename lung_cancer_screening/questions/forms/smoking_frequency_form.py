from django import forms

from ..models.smoking_frequency_response import SmokingFrequencyResponse, SmokingFrequencyValues

from ...nhsuk_forms.typed_choice_field import TypedChoiceField

class SmokingFrequencyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = TypedChoiceField(
            choices=SmokingFrequencyValues.choices,
            widget=forms.RadioSelect,
            label="How often do you smoke cigarettes?",
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
