from django.db import models

from ..models.tobacco_smoking_history import TobaccoSmokingHistory

from .base import BaseModel

class SmokingFrequencyValues(models.TextChoices):
    DAILY = "D", "Daily"
    WEEKLY = "W", "Weekly"
    MONTHLY = "M", "Monthly"

class SmokingFrequencyResponse(BaseModel):
    tobacco_smoking_history = models.OneToOneField(
        TobaccoSmokingHistory,
        on_delete=models.CASCADE,
        related_name='smoking_frequency_response'
    )

    value = models.CharField(
            max_length=1,
            choices=SmokingFrequencyValues.choices
    )
