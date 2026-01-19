from django.db import models
from django.contrib.postgres.fields import ArrayField

from .validators.singleton_option import validate_singleton_option
from .base import BaseModel
from .response_set import ResponseSet


class EducationValues(models.TextChoices):
    FINISHED_SCHOOL_BEFORE_15 = "X", "I finished school before the age of 15"
    GCSES = "G", "GCSEs"
    A_LEVELS = "A", "A-levels"
    FURTHER_EDUCATION = "F", "Further education"
    BACHELORS_DEGREE = "B", "Bachelor's degree"
    POSTGRADUATE_DEGREE = "P", "Postgraduate degree"
    PREFER_NOT_TO_SAY = "N", "I'd prefer not to say"


class EducationResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='education_response')
    value = ArrayField(
        models.CharField(max_length=1, choices=EducationValues.choices),
        validators=[
            validate_singleton_option
        ]
    )
