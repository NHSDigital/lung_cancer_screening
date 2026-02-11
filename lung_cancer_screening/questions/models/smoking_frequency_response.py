from django.db import models

from ..models.tobacco_smoking_history import TobaccoSmokingHistory

from .base import BaseModel

class SmokingFrequencyValues(models.TextChoices):
    DAILY = "D", "Daily"
    WEEKLY = "W", "Weekly"
    MONTHLY = "M", "Monthly"

class SmokingFrequencyResponse(BaseModel):
    SINGULAR_TEXT_MAP = {
        SmokingFrequencyValues.DAILY: "day",
        SmokingFrequencyValues.WEEKLY: "week",
        SmokingFrequencyValues.MONTHLY: "month",
    }

    tobacco_smoking_history = models.OneToOneField(
        TobaccoSmokingHistory,
        on_delete=models.CASCADE,
        related_name='smoking_frequency_response'
    )
    value = models.CharField(
            max_length=1,
            choices=SmokingFrequencyValues.choices
    )

    def get_value_display_as_singleton_text(self):
        return self.SINGULAR_TEXT_MAP.get(self.value)
