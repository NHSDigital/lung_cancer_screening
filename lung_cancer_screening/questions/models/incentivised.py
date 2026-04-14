
from django.db import models

from .base import BaseModel
from .response_set import ResponseSet


class Incentivised(BaseModel):
    user = models.ForeignKey('questions.User', on_delete=models.CASCADE, related_name='incentivised_records')
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='incentivised_record')

    incentivised_at = models.DateTimeField(auto_now_add=True)

class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=["user"],
            name="unique_incentive_per_user",
        )
    ]
