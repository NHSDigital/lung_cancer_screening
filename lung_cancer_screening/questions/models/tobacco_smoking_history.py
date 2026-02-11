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


NO_CHANGE_VALUE = "no_change"
class TobaccoSmokingHistory(BaseModel):
    class Levels(models.TextChoices):
        NORMAL = "normal", "Normal"
        INCREASED = "increased", "Yes, I used to smoke more"
        DECREASED = "decreased", "Yes, I used to smoke fewer"

        # Only used to populate values in the form
        STOPPED = "stopped", "Yes, I stopped smoking for a period of 1 year or longer"
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
