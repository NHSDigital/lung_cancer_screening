from django.db import models

from .base import BaseModel
from .tobacco_smoking_history import TobaccoSmokingHistory

class SmokingCurrentResponse(BaseModel):
    tobacco_smoking_history = models.OneToOneField(
        TobaccoSmokingHistory,
        on_delete=models.CASCADE,
        related_name='smoking_current_response')

    value = models.BooleanField()
