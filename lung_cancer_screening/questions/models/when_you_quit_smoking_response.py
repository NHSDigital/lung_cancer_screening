from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from .base import BaseModel
from .response_set import ResponseSet

class WhenYouQuitSmokingResponse(BaseModel):
    response_set = models.OneToOneField(
        ResponseSet,
        on_delete=models.CASCADE,
        related_name="when_you_quit_smoking_response",
    )
    value = models.IntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )

    def clean(self):
        super().clean()
        self.validates_date_of_birth_response()
        self.validates_age_started_smoking_response()


    def validates_date_of_birth_response(self):
        if not hasattr(self.response_set, "date_of_birth_response"):
            raise ValidationError({
                "value": ValidationError(
                    "date of birth not set",
                    code="no_date_of_birth"
                )
            })


    def validates_age_started_smoking_response(self):
        if not hasattr(self.response_set, "age_when_started_smoking_response"):
            raise ValidationError({
                "value": ValidationError(
                    "age started smoking not set",
                    code="no_age_started_smoking"
                )
            })
