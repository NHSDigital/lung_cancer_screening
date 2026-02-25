from django.db import models
from django.db.models import Case, Value, When
from django.core.exceptions import ValidationError

from .base import BaseModel, BaseQuerySet
from .response_set import ResponseSet

class TobaccoSmokingHistoryTypes(models.TextChoices):
    CIGARETTES = "Cigarettes", "Cigarettes"
    ROLLED_CIGARETTES = "RolledCigarettes", "Rolled cigarettes, or roll-ups"
    PIPE = "Pipe", "Pipe"
    CIGARS = "Cigars", "Cigars"
    CIGARILLOS = "Cigarillos", "Cigarillos"
    SHISHA = "Shisha", "Shisha"

class TobaccoSmokingHistoryQuerySet(BaseQuerySet):
    def in_form_order(self):
        form_order = [choice[0] for choice in TobaccoSmokingHistoryTypes.choices]
        order = Case(
            *[When(type=type_val, then=Value(i)) for i, type_val in enumerate(form_order)],
            default=Value(len(form_order)),
        )
        return self.order_by(order)

    def increased(self):
        return self.filter(level='increased')

    def decreased(self):
        return self.filter(level='decreased')

    def normal(self):
        return self.filter(level='normal')

    def grouped_by_type(self):
        """Return a dict mapping type -> queryset of TobaccoSmokingHistory for that type (in form order)."""
        form_order = [choice[0] for choice in TobaccoSmokingHistoryTypes.choices]
        return {
            type_val: self.filter(type=type_val).in_form_order()
            for type_val in form_order
        }

    def cigarettes(self):
        return self.filter(type=TobaccoSmokingHistoryTypes.CIGARETTES)

    def cigars(self):
        return self.filter(type=TobaccoSmokingHistoryTypes.CIGARS)

    def rolled_cigarettes(self):
        return self.filter(type=TobaccoSmokingHistoryTypes.ROLLED_CIGARETTES)

    def pipe(self):
        return self.filter(type=TobaccoSmokingHistoryTypes.PIPE)

    def cigarillos(self):
        return self.filter(type=TobaccoSmokingHistoryTypes.CIGARILLOS)


NO_CHANGE_VALUE = "no_change"
class TobaccoSmokingHistory(BaseModel):
    class Levels(models.TextChoices):
        NORMAL = "normal", "Normal"
        INCREASED = "increased", "Yes, I used to smoke more"
        DECREASED = "decreased", "Yes, I used to smoke fewer"

        # Only used to populate values in the form
        NO_CHANGE = NO_CHANGE_VALUE, "No, it has not changed"


    response_set = models.ForeignKey(
        ResponseSet,
        on_delete=models.CASCADE,
        related_name="tobacco_smoking_history",
    )
    type = models.CharField(
        choices=TobaccoSmokingHistoryTypes.choices
    )
    level = models.CharField(
        choices=Levels.choices,
        default=Levels.NORMAL,
        max_length=20,
    )

    objects = TobaccoSmokingHistoryQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["response_set", "type", "level"],
                name="unique_tobacco_smoking_history_per_response_set_and_type_and_level",
                violation_error_message="A tobacco smoking history already exists for this response set, type and level",
            ),
        ]

    def clean(self):
        super().clean()
        self._validate_no_change_and_other_levels()

    def _validate_no_change_and_other_levels(self):
        others = self.response_set.tobacco_smoking_history.filter(type=self.type).exclude(pk=self.pk)
        if self.level == NO_CHANGE_VALUE:
            if others.exclude(level__in=[NO_CHANGE_VALUE, self.Levels.NORMAL]).exists():
                raise ValidationError(
                    {"level": "Cannot have both no change and other levels selected"}
                )
        elif self.level != self.Levels.NORMAL:
            if others.filter(level=NO_CHANGE_VALUE).exists():
                raise ValidationError(
                    {"level": "Cannot have both no change and other levels selected"}
                )

    def human_type(self):
        return TobaccoSmokingHistoryTypes(self.type).label

    def amount(self):
        if hasattr(self, "smoked_amount_response"):
            return self.smoked_amount_response.value
        else:
            return None

    def frequency_singular(self):
        if hasattr(self, "smoking_frequency_response"):
            return self.smoking_frequency_response.get_value_display_as_singleton_text()
        else:
            return None

    def duration_years(self):
        if hasattr(self, "smoked_total_years_response"):
            return self.smoked_total_years_response.value
        else:
            return None

    def is_increased(self):
        return self.level == self.Levels.INCREASED

    def is_decreased(self):
        return self.level == self.Levels.DECREASED

    def is_normal(self):
        return self.level == self.Levels.NORMAL

    def is_current(self):
        if hasattr(self, "smoking_current_response"):
            return self.smoking_current_response.value
        else:
            return None

