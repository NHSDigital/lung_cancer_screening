from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

from .base import BaseModel
from .response_set import ResponseSet


class WeightResponse(BaseModel):
    MIN_WEIGHT_METRIC = 254
    MAX_WEIGHT_METRIC = 3175
    MAX_WEIGHT_IMPERIAL = 700
    MIN_WEIGHT_IMPERIAL = 56

    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='weight_response')

    metric = models.PositiveIntegerField(null=True, blank=True, validators=[
        MinValueValidator(MIN_WEIGHT_METRIC, message="Weight must be between 25.4kg and 317.5kg"),
        MaxValueValidator(MAX_WEIGHT_METRIC, message="Weight must be between 25.4kg and 317.5kg"),
    ])
    imperial = models.PositiveIntegerField(null=True, blank=True, validators=[
        MinValueValidator(MIN_WEIGHT_IMPERIAL, message="Weight must be between 4 stone and 50 stone"),
        MaxValueValidator(MAX_WEIGHT_IMPERIAL, message="Weight must be between 4 stone and 50 stone"),
    ])

    def clean(self):
        if not self.metric and not self.imperial:
            raise ValidationError("Either metric or imperial weight must be provided.")
        if self.metric and self.imperial:
            raise ValidationError("Cannot provide both metric and imperial weight.")

    @property
    def formatted(self):
        if self.metric:
            return f"{Decimal(self.metric) / 10}kg"
        elif self.imperial:
            value = Decimal(self.imperial)
            return f"{value // 14} stone {value % 14} pounds"
        return None
