from django import forms
from inflection import camelize

from ...nhsuk_forms.choice_field import MultipleChoiceField
from ..models.tobacco_smoking_history import TobaccoSmokingHistory


class SmokingChangeForm(forms.Form):
    def __init__(self, *args, response_set, tobacco_type, **kwargs):
        super().__init__(*args, **kwargs)

        self.response_set = response_set
        self.tobacco_type = camelize(tobacco_type)

        self.fields["value"] = MultipleChoiceField(
            choices=self.choices(),
            widget=forms.CheckboxSelectMultiple,
            label="Has the number of cigarettes you normally smoke changed over time?",
            label_classes="nhsuk-fieldset__legend--l",
            label_is_page_heading=True,
            hint="Select all that apply",
            error_messages={
                "required": self._required_error_message()
            },
        )

        self.fields["value"].initial = self._existing_levels()

        value_field = self["value"]
        value_field.add_divider_after(
            TobaccoSmokingHistory.Levels.STOPPED, "or"
        )

    def choices(self):
        return [
            (value, label)
            for value, label in TobaccoSmokingHistory.Levels.choices
            if value != TobaccoSmokingHistory.Levels.NORMAL
        ]


    def _required_error_message(self):
        return "Select if the number of cigarettes you smoke has changed over time"


    def save(self, commit=True):
        if not self.is_valid():
            return None

        self._delete_levels_not_selected()
        return self._create_levels_selected()


    def is_valid(self):
        if not super().is_valid() :
            return False
        if (self.cleaned_data["value"].count(TobaccoSmokingHistory.Levels.NO_CHANGE) > 0
            and len(self.cleaned_data["value"]) > 1):
                self.add_error( "value", forms.ValidationError("Select if the number of cigarettes you smoke has changed over time, or select 'no, it has not changed'"))
                return False
        return True

    def _delete_levels_not_selected(self):
        for level in self._existing_levels():
            if level not in self.cleaned_data["value"]:
                self.response_set.tobacco_smoking_history.filter(
                    type=self.tobacco_type,
                    level=level
                ).delete()


    def _create_levels_selected(self):
        instances = [
            TobaccoSmokingHistory(
                response_set=self.response_set,
                type=self.tobacco_type,
                level=level,
            )
            for level in self.cleaned_data["value"]
            if level not in self._existing_levels()
        ]

        # Force validation errors if there are any
        for instance in instances:
            instance.full_clean()

        TobaccoSmokingHistory.objects.bulk_create(instances)

        return instances


    def _existing_levels(self):
        return list(self.response_set.tobacco_smoking_history.exclude(
            level=TobaccoSmokingHistory.Levels.NORMAL
        ).values_list("level", flat=True))
