from django.db import models

from .base import BaseModel
from .response_set import ResponseSet


class AsbestosExposureResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='asbestos_exposure_response')
    value = models.BooleanField()
