from django.db import models
from django.db.models import Case, Value, When

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


class TobaccoSmokingHistory(BaseModel):
    response_set = models.ForeignKey(
        ResponseSet,
        on_delete=models.CASCADE,
        related_name="tobacco_smoking_history",
    )
    type = models.CharField(
        choices=TobaccoSmokingHistoryTypes.choices
    )

    objects = TobaccoSmokingHistoryQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["response_set", "type"],
                name="unique_tobacco_smoking_history_per_response_set",
                violation_error_message="A tobacco smoking history already exists for this response set and type"
            )
        ]

    def human_type(self):
        return TobaccoSmokingHistoryTypes(self.type).label
