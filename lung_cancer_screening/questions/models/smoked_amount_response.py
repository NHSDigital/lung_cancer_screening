from django.db import models
from django.core.validators import MinValueValidator

from .base import BaseModel
from .tobacco_smoking_history import TobaccoSmokingHistory


class SmokedAmountResponse(BaseModel):
    tobacco_smoking_history = models.OneToOneField(
        TobaccoSmokingHistory,
        on_delete=models.CASCADE,
        related_name='smoked_amount_response'
    )
    value = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
