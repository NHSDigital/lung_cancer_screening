from django.db import models

from .base import BaseModel
from .response_set import ResponseSet


class SexAtBirthValues(models.TextChoices):
    FEMALE = "F", 'Female'
    MALE = "M", 'Male'


class SexAtBirthResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='sex_at_birth_response')
    value = models.CharField(max_length=1, choices=SexAtBirthValues.choices)
