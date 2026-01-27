from django.db import models

from .base import BaseModel
from .response_set import ResponseSet


class CurrentlySmokingCigarettesResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='currently_smoking_cigarettes_response')
    value = models.BooleanField()
