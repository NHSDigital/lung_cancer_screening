from django.db import models

from .base import BaseModel
from .response_set import ResponseSet


class EthnicityValues(models.TextChoices):
    ASIAN = "A", "Asian or Asian British"
    BLACK = "B", "Black, African, Caribbean or Black British"
    MIXED = "M", "Mixed or multiple ethnic groups"
    WHITE = "W", "White"
    OTHER = "O", "Other ethnic group"
    PREFER_NOT_TO_SAY = "N", "Prefer not to say"


class EthnicityResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='ethnicity_response')
    value = models.CharField(max_length=1, choices=EthnicityValues.choices)
