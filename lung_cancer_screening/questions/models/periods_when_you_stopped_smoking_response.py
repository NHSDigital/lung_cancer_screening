from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .base import BaseModel
from .response_set import ResponseSet


class PeriodsWhenYouStoppedSmokingResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='periods_when_you_stopped_smoking_response')
    value = models.BooleanField()
    duration_years = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1, message="The number of years you stopped smoking for must be at least 1")
        ]
    )

    def clean(self):
        super().clean()
        self._validate_duration_years_not_set_if_value_is_false()
        self._validate_duration_years()
        self._validate_has_answered_age_started_smoking()
        self._validate_duration_years_is_less_than_time_they_have_smoked()


    def _validate_duration_years_not_set_if_value_is_false(self):
        if self.value is False and self.duration_years is not None:
            raise ValidationError(
                {
                    "duration_years": "duration_years must not be present if value is false"
                }
            )


    def _validate_duration_years(self):
        if self.value and not self.duration_years:
            raise ValidationError(
                {
                    "duration_years": "Enter the total number of years you stopped smoking"
                }
            )

    def _validate_has_answered_age_started_smoking(self):
        if self.value and not hasattr(self.response_set, "age_when_started_smoking_response"):
            raise ValidationError({
                "value": ValidationError(
                    "age started smoking not set",
                    code="no_age_started_smoking"
                )
            })

    def _validate_duration_years_is_less_than_time_they_have_smoked(self):
        if not self.value:
            return None

        if self.duration_years > self.response_set.age_when_started_smoking_response.years_smoked_including_stopped():
            raise ValidationError(
                {
                    "duration_years": "The number of years you stopped smoking must be fewer than the total number of years you have been smoking"
                }
            )
