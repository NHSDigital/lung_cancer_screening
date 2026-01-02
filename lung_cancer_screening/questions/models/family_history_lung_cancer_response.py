from django.db import models

from .base import BaseModel
from .response_set import ResponseSet


class FamilyHistoryLungCancerValues(models.TextChoices):
    YES = "Y", 'Yes'
    NO = "N", 'No'
    UNKNOWN = "U", "I do not know"

class FamilyHistoryLungCancerResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='family_history_lung_cancer')
    value = models.CharField(max_length=1, choices=FamilyHistoryLungCancerValues.choices)
