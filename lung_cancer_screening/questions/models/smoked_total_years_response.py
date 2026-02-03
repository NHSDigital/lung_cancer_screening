from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .base import BaseModel
from .tobacco_smoking_history import TobaccoSmokingHistory


class SmokedTotalYearsResponse(BaseModel):
    tobacco_smoking_history = models.OneToOneField(
        TobaccoSmokingHistory,
        on_delete=models.CASCADE,
        related_name='smoked_total_years_response'
    )

    value = models.IntegerField(
        validators=[
            MinValueValidator(1, message="The number of years you smoked cigarettes must be at least 1")
        ]
    )


    def clean(self):
        super().clean()
        self._validate_age_when_started_smoking_response_exists()
        self._validate_value_fewer_than_total_number_of_years_smoked()


    def _validate_age_when_started_smoking_response_exists(self):
        if not hasattr(self.tobacco_smoking_history.response_set, 'age_when_started_smoking_response'):
            raise ValidationError({
                "value": ValidationError(
                    "You must answer age when started smoking before answering how many years you have smoked cigarettes",
                    code="age_when_started_smoking_response_not_found"
                )
            })

    def _validate_value_fewer_than_total_number_of_years_smoked(self):
        if not self.value:
            return None

        if self.value > self.tobacco_smoking_history.response_set.age_when_started_smoking_response.years_smoked_including_stopped():
            raise ValidationError({
                "value": ValidationError(
                    "The number of years you smoked cigarettes must be fewer than the total number of years you have been smoking",
                    code="value_greater_than_total_number_of_years_smoked"
                )
            })
