import json

from django.db import models
from django.forms import ValidationError
from django.utils import timezone

from .base import BaseModel
from .response_set import ResponseSet

from django.core.validators import MaxValueValidator, MinValueValidator



# def validate_less_than_age(self, value):
#     print(f"self : {self}")
#     print(f"value : {self.value}")
#     print("what")
#     print(f"dob : {self.response_set.date_of_birth}")
#     print(hasattr(self.response_set, "date_of_birth"))
#     if hasattr(self.response_set, "date_of_birth") :
#         if value < self.get_age :
#             raise ValidationError(
#                 "Must be less than your age",
#                 code="less_than_age",
#             )

class AgeWhenStartedSmokingResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='age_when_started_smoking_response')
    value = models.PositiveIntegerField(validators=[
        MinValueValidator(1, message="The age you started smoking must be between 1 and your current age"),
        # validate_less_than_age
    ]
    )

    # def clean(self):
    #     super().clean()
    #     print(f"clean 1:{self.response_set}")
    #     if hasattr(self.response_set, "date_of_birth_response") :
    #         print(f"clean 2:{self.response_set.date_of_birth_response.value}")
    #         today = timezone.now()
    #         born = self.response_set.date_of_birth_response.value
    #         age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    #         print(f"value : {self.value}")
    #         print(f"Age {age}")
    #         if (self.value and self.value < age):
    #             raise ValidationError(
    #                 "The age you started smoking must be the same as, or younger than your current age"
    #         )
            #if submitted_response_sets_in_last_year:
            #    raise ValidationError(
            #        "Responses have already been submitted for this user"
            #    )

