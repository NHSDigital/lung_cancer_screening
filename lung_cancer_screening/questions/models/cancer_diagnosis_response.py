from django.db import models

from .base import BaseModel
from .response_set import ResponseSet


class CancerDiagnosisResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='cancer_diagnosis_response')
    value = models.BooleanField()
