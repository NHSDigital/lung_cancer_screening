from django.db import models

from .base import BaseModel
from .response_set import ResponseSet


class GenderValues(models.TextChoices):
    FEMALE = "F", 'Female'
    MALE = "M", 'Male'
    NON_BINARY = "N", 'Non-binary'
    PREFER_NOT_TO_SAY = "P", 'Prefer not to say'
    GP = "G", 'How I describe myself may not match my GP record'


class GenderResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='gender_response')
    value = models.CharField(max_length=1, choices=GenderValues.choices)
