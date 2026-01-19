from django.db import models
from django.contrib.postgres.fields import ArrayField

from .validators.singleton_option import validate_singleton_option
from .base import BaseModel
from .response_set import ResponseSet


class RespiratoryConditionValues(models.TextChoices):
    PNEUMONIA = "P", "Pneumonia"
    EMPHYSEMA = "E", "Emphysema"
    BRONCHITIS = "B", "Bronchitis"
    TUBERCULOSIS = "T", "Tuberculosis (TB)"
    COPD = "C", "Chronic obstructive pulmonary disease (COPD)"
    NONE = "N", "No, I have not had any of these respiratory conditions"


class RespiratoryConditionsResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='respiratory_conditions_response')
    value = ArrayField(
        models.CharField(max_length=1, choices=RespiratoryConditionValues.choices),
        validators=[
            validate_singleton_option
        ]
    )
