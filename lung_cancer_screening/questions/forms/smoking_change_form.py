from django import forms

from ...nhsuk_forms.choice_field import MultipleChoiceField
from ..models.tobacco_smoking_history import TobaccoSmokingHistory
from .mixins.smoking_form_presenter import SmokingFormPresenter


class SmokingChangeForm(SmokingFormPresenter, forms.Form):
    def __init__(self, *args, response_set, tobacco_smoking_history_item, **kwargs):
        super().__init__(*args, **kwargs)

        self.response_set = response_set
        self.tobacco_smoking_history = tobacco_smoking_history_item
        self.tobacco_type = tobacco_smoking_history_item.type

        self.fields["value"] = MultipleChoiceField(
            choices=self.choices(),
            widget=forms.CheckboxSelectMultiple,
            label=self.label(),
            label_classes="nhsuk-fieldset__legend--l",
            label_is_page_heading=True,
            hint="Select all that apply",
            error_messages={
                "required": self.required_error_message()
            },
        )

        self.fields["value"].initial = self._existing_levels()

        value_field = self["value"]
        value_field.add_divider_after(
            TobaccoSmokingHistory.Levels.DECREASED, "or"
        )

    def current_label(self):
        return (
            f"Has the number of {self.tobacco_smoking_history.unit()} "
            "you normally smoke changed over time?"
        )


    def previous_label(self):
        return (
            f"Did the number of {self.tobacco_smoking_history.unit()} "
            "you normally smoke change over time?"
        )


    def label(self):
        if self.tobacco_smoking_history.is_current():
            return self.current_label()
        else:
            return self.previous_label()


    def choices(self):
        return [
            (value, self.generate_label(value, label))
            for value, label in TobaccoSmokingHistory.Levels.choices
            if value != TobaccoSmokingHistory.Levels.NORMAL
        ]

    def generate_label(self, value, label):
        if value == TobaccoSmokingHistory.Levels.NO_CHANGE:
            return label

        return (
            f"{TobaccoSmokingHistory.Levels(value).label} "
            f" than {self.presenter.to_sentence()}"
        )

    def required_error_message(self):
        return (
            f"Select if the number of {self.tobacco_smoking_history.unit()} "
            f"you {self.presenter.smoke_or_smoked()} has changed over time"
        )


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
                message = (
                    f"{self.required_error_message()}, or select 'no, it has not changed'"
                )
                self.add_error( "value", forms.ValidationError(message))
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
        return list(self.response_set.tobacco_smoking_history.filter(
            type=self.tobacco_type
        ).exclude(
            level=TobaccoSmokingHistory.Levels.NORMAL
        ).values_list("level", flat=True))
