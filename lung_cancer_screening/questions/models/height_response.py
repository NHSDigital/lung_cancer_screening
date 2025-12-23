from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from .base import BaseModel
from .response_set import ResponseSet


class HeightResponse(BaseModel):
    MAX_HEIGHT_METRIC = 2438
    MIN_HEIGHT_METRIC = 1397
    MAX_HEIGHT_IMPERIAL = 96
    MIN_HEIGHT_IMPERIAL = 55

    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='height_response')

    metric = models.PositiveIntegerField(null=True, blank=True, validators=[
        MinValueValidator(MIN_HEIGHT_METRIC, message="Height must be between 139.7cm and 243.8 cm"),
        MaxValueValidator(MAX_HEIGHT_METRIC, message="Height must be between 139.7cm and 243.8 cm"),
    ])
    imperial = models.PositiveIntegerField(null=True, blank=True, validators=[
        MinValueValidator(MIN_HEIGHT_IMPERIAL, message="Height must be between 4 feet 7 inches and 8 feet"),
        MaxValueValidator(MAX_HEIGHT_IMPERIAL, message="Height must be between 4 feet 7 inches and 8 feet"),
    ])

    def clean(self):
        if not self.metric and not self.imperial:
            raise ValidationError("Either metric or imperial height must be provided.")
        if self.metric and self.imperial:
            raise ValidationError("Cannot provide both metric and imperial height.")
