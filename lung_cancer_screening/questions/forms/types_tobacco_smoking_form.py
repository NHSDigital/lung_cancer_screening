from django import forms

from lung_cancer_screening.questions.models.smoked_total_years_response import SmokedTotalYearsResponse
from lung_cancer_screening.questions.models.smoking_current_response import SmokingCurrentResponse

from ...nhsuk_forms.choice_field import MultipleChoiceField
from ..models.tobacco_smoking_history import (
    TobaccoSmokingHistory,
    TobaccoSmokingHistoryTypes,
)


class TypesTobaccoSmokingForm(forms.Form):

    value = MultipleChoiceField(
        choices=TobaccoSmokingHistoryTypes.choices,
        widget=forms.CheckboxSelectMultiple,
        label="What do you or have you smoked?",
        label_classes="nhsuk-fieldset__legend--m",
        hint="Select all that apply",
        error_messages={
            "required": "Select the type of tobacco you smoke or have smoked"
        },
    )

    def __init__(self, *args, response_set, **kwargs):
        super().__init__(*args, **kwargs)
        self.response_set = response_set
        self.existing_types = list(
            response_set.tobacco_smoking_history.values_list('type', flat=True)
        )
        self.fields["value"].initial = self.existing_types

        value_field=self['value']
        value_field.add_hint_for_choice(
            TobaccoSmokingHistoryTypes.ROLLING_TOBACCO,
            "or roll-ups",
        )
        value_field.add_hint_for_choice(
            TobaccoSmokingHistoryTypes.SMALL_CIGARS,
            "Petit Corona or Short Panetela, usually 4 to 5 inches long",
        )
        value_field.add_hint_for_choice(
            TobaccoSmokingHistoryTypes.MEDIUM_CIGARS,
            "Robusto or Corona, usually 5 to 6 inches long",
        )
        value_field.add_hint_for_choice(
            TobaccoSmokingHistoryTypes.LARGE_CIGARS,
            "Churchill or Double Corona, usually 7 to 8 inches long",
        )
        value_field.add_hint_for_choice(
            TobaccoSmokingHistoryTypes.CIGARILLOS,
            "Cafe Creme or Signature cigars, roughly the size of a cigarette"
        )


    def save(self, commit=True):
        if not self.is_valid():
            return None

        self._delete_types_not_selected()
        return self._create_types_selected()


    def _delete_types_not_selected(self):
        for kind in self.existing_types:
            if kind not in self.cleaned_data["value"]:
                TobaccoSmokingHistory.objects.filter(response_set=self.response_set, type=kind).delete()


    def _create_types_selected(self):
        instances = [
            TobaccoSmokingHistory(
                response_set=self.response_set,
                type=kind,
                level=TobaccoSmokingHistory.Levels.NORMAL,
            )
            for kind in self.cleaned_data["value"]
            if kind not in self.existing_types
        ]

        for instance in instances:
            instance.full_clean()

        TobaccoSmokingHistory.objects.bulk_create(instances)

        self._create_default_responses_for_single_selection()

        return instances

    def _create_default_responses_for_single_selection(self):
        response_set = self.response_set
        instances = response_set.tobacco_smoking_history
        if instances.count() == 1:
            instance = instances.first()

            SmokingCurrentResponse.objects.update_or_create(
                tobacco_smoking_history=instance,
                defaults={
                    "value": response_set.current_smoker()
                },
            )

            SmokedTotalYearsResponse.objects.update_or_create(
                tobacco_smoking_history=instance,
                defaults={
                    "value": response_set.age_when_started_smoking_response.years_smoked_including_stopped()
                }
            )
