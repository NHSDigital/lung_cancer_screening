from django.db import models

from .base import BaseModel
from .response_set import ResponseSet


class TobaccoSmokingHistoryTypes(models.TextChoices):
    CIGARETTES = "Cigarettes", "Cigarettes"
    ROLLED_CIGARETTES = "RolledCigarettes", "Rolled cigarettes, or roll-ups"
    PIPE = "Pipe", "Pipe"
    CIGARS = "Cigars", "Cigars"
    CIGARILLOS = "Cigarillos", "Cigarillos"
    SHISHA = "Shisha", "Shisha"


class TobaccoSmokingHistory(BaseModel):
    response_set = models.ForeignKey(
        ResponseSet,
        on_delete=models.CASCADE,
        related_name="tobacco_smoking_history",
    )
    type = models.CharField(
        choices=TobaccoSmokingHistoryTypes.choices
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["response_set", "type"],
                name="unique_tobacco_smoking_history_per_response_set",
                violation_error_message="A tobacco smoking history already exists for this response set and type"
            )
        ]
