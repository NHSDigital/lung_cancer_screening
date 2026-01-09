from django import forms

from ...nhsuk_forms.choice_field import MultipleChoiceField
from ..models.respiratory_conditions_response import RespiratoryConditionsResponse, RespiratoryConditionValues


class RespiratoryConditionsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["value"] = MultipleChoiceField(
            choices=RespiratoryConditionValues.choices,
            widget=forms.CheckboxSelectMultiple,
            label=(
                "Have you ever been diagnosed with any of the following "
                "respiratory conditions?"
            ),
            label_classes="nhsuk-fieldset__legend--l",
            label_is_page_heading=True,
            hint="Select all that apply",
            error_messages={
                'required': (
                    'Select if you have had any respiratory conditions'
                ),
                'singleton_option': (
                    'Select if you have had any respiratory conditions, '
                    'or select \'No, I have not had any of these '
                    'respiratory conditions\''
                )
            }
        )

        # Add hints for each choice
        respiratory_conditions_field = self["value"]
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
            (
                "An inflammation of the airways in the lungs that is "
                "usually caused by an infection"
            )
        )
        respiratory_conditions_field.add_hint_for_choice(
            RespiratoryConditionValues.TUBERCULOSIS,
            (
                "An infection that usually affects the lungs, but can "
                "affect any part of the body"
            )
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
        model = RespiratoryConditionsResponse
        fields = ['value']
