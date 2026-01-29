from django.db import models

from .base import BaseModel
from .tobacco_smoking_history import TobaccoSmokingHistory


class SmokedTotalYearsResponse(BaseModel):
    tobacco_smoking_history = models.OneToOneField(
        TobaccoSmokingHistory,
        on_delete=models.CASCADE,
        related_name='smoked_total_years_response'
    )
    value = models.IntegerField()
