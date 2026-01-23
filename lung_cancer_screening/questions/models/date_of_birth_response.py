from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta

from .base import BaseModel
from .response_set import ResponseSet


class DateOfBirthResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='date_of_birth_response')
    value = models.DateField()

    def is_currently_in_age_range(self):
        fifty_five_years_ago = date.today() - relativedelta(years=55)
        seventy_five_years_ago = date.today() - relativedelta(years=75)

        return seventy_five_years_ago < self.value <= fifty_five_years_ago

    def age_in_years(self):
        today = date.today()
        born = self.value
        age = int(today.year - born.year - ((today.month, today.day) < (born.month, born.day)))
        return age
