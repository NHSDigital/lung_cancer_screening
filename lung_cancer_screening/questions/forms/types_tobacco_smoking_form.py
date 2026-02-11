from django import forms

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

        return instances
