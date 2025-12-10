from django import forms

from ...nhsuk_forms.choice_field import MultipleChoiceField
from ..models.response_set import ResponseSet, RespiratoryConditionValues


class RespiratoryConditionsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.instance.user = self.user

        self.fields["respiratory_conditions"] = MultipleChoiceField(
            choices=RespiratoryConditionValues.choices,
            widget=forms.CheckboxSelectMultiple,
            label="Have you ever been diagnosed with any of the following respiratory conditions?",
            label_classes="nhsuk-fieldset__legend--l",
            hint="Select all that apply",
            error_messages={
                'required': 'Select if you have had any respiratory conditions',
                'singleton_option': 'Select if you have had any respiratory conditions, or select \'No, I have not had any of these respiratory conditions\''
            }
        )

        # Add hints for each choice
        respiratory_conditions_field = self["respiratory_conditions"]
        respiratory_conditions_field.add_hint_for_choice(
            RespiratoryConditionValues.PNEUMONIA,
            "An infection of the lungs, usually diagnosed by a chest x-ray"
        )
        respiratory_conditions_field.add_hint_for_choice(
            RespiratoryConditionValues.EMPHYSEMA,
            "Damage to the air sacs in the lungs"
        )
        respiratory_conditions_field.add_hint_for_choice(
            RespiratoryConditionValues.BRONCHITIS,
            "An inflammation of the airways in the lungs that is usually caused by an infection"
        )
        respiratory_conditions_field.add_hint_for_choice(
            RespiratoryConditionValues.TUBERCULOSIS,
            "An infection that usually affects the lungs, but can affect any part of the body"
        )
        respiratory_conditions_field.add_hint_for_choice(
            RespiratoryConditionValues.COPD,
            "A group of lung conditions that cause breathing difficulties"
        )

        # Add divider before "None of the above"
        respiratory_conditions_field.add_divider_after(
            RespiratoryConditionValues.COPD,
            "or"
        )

    class Meta:
        model = ResponseSet
        fields = ['respiratory_conditions']
