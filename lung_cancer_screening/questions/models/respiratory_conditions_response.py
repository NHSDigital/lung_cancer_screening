from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError

from .base import BaseModel
from .response_set import ResponseSet


class RespiratoryConditionValues(models.TextChoices):
    PNEUMONIA = "P", "Pneumonia"
    EMPHYSEMA = "E", "Emphysema"
    BRONCHITIS = "B", "Bronchitis"
    TUBERCULOSIS = "T", "Tuberculosis (TB)"
    COPD = "C", "Chronic obstructive pulmonary disease (COPD)"
    NONE = "N", "No, I have not had any of these respiratory conditions"


def validate_singleton_option(value):
    if value and "N" in value and len(value) > 1:
        raise ValidationError(
            "Cannot have singleton value and other values selected",
            code="singleton_option",
        )


class RespiratoryConditionsResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='respiratory_conditions_response')
    value = ArrayField(
        models.CharField(max_length=1, choices=RespiratoryConditionValues.choices),
        validators=[validate_singleton_option]
    )

    @property
    def formatted(self):
        if not self.value:
            return None
        display_values = [
            RespiratoryConditionValues(code).label
            for code in self.value
        ]
        return ", ".join(display_values)
