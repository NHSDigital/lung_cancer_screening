from django.db import models

from .base import BaseModel
from .response_set import ResponseSet


class DateOfBirthResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='date_of_birth_response')
    value = models.DateField()
