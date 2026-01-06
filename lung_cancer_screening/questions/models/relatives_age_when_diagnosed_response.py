from django.db import models

from .base import BaseModel
from .response_set import ResponseSet


class RelativesAgeWhenDiagnosedValues(models.TextChoices):
    YES = "Y", "Yes, they were younger than 60"
    NO = "N", "No, they were 60 or older"
    UNKNOWN = "U", "I do not know"

class RelativesAgeWhenDiagnosedResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='relatives_age_when_diagnosed')
    value = models.CharField(max_length=1, choices=RelativesAgeWhenDiagnosedValues.choices)
