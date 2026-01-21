from django.db import models
from django.core.exceptions import ValidationError

from .base import BaseModel
from .response_set import ResponseSet


class PeriodsWhenYouStoppedSmokingResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='periods_when_you_stopped_smoking_response')
    value = models.BooleanField()
    duration_years = models.IntegerField(null=True, blank=True)

    def clean(self):
        super().clean()
        self._validate_duration_years()


    def _validate_duration_years(self):
        if self.value and not self.duration_years:
            raise ValidationError(
                {
                    "duration_years": "Enter the total number of years you stopped smoking for"
                }
            )
