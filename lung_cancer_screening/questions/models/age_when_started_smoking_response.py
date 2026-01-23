from django.db import models
from django.forms import ValidationError

from .base import BaseModel
from .response_set import ResponseSet

from django.core.validators import MinValueValidator

class AgeWhenStartedSmokingResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name="age_when_started_smoking_response")
    value = models.PositiveIntegerField(validators=[
        MinValueValidator(1, message="The age you started smoking must be between 1 and your current age")
    ]
    )

    def clean(self):
        super().clean()
        if hasattr(self.response_set, "date_of_birth_response") :
            if (self.value and self.value > self.response_set.date_of_birth_response.age_in_years()):
                raise ValidationError({
                    "value":ValidationError(
                        "age started smoking must be less than current age",
                        code="age_started_smoking_greater_than_current_age")
                }
                )
        else:
            raise ValidationError({
                    "value":ValidationError(
                        "date of birth not set",
                        code="no_date_of_birth")
                }
                )
