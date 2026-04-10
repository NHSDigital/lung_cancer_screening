from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
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
        self.validate_age_when_quit_smoking_greater_than_current_age()
        self.validates_age_started_smoking_response()
        self.validates_age_when_quit_smoking_greater_than_age_started()


    def validates_date_of_birth_response(self):
        if not hasattr(self.response_set, "date_of_birth_response"):
            raise ValidationError({
                "value": ValidationError(
                    "date of birth not set",
                    code="no_date_of_birth"
                )
            })

    def validate_age_when_quit_smoking_greater_than_current_age(self):
        if self.value and self.response_set.date_of_birth_response.age_in_years() < self.value:
            raise ValidationError({
                "value": ValidationError(
                    "age when you quit smoking cannot be greater than current age",
                    code="age_when_quit_smoking_greater_than_current_age"

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

    def validates_age_when_quit_smoking_greater_than_age_started(self):
        if self.value and self.response_set.age_when_started_smoking_response.value > self.value:
            raise ValidationError({
                "value": ValidationError(
                    "age when you quit smoking cannot be lower than age started smoking",
                    code="age_when_quit_smoking_greater_than_age_started"

                )
            })
