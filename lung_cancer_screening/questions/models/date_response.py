from django.db import models
from .base import BaseModel
from .participant import Participant

class DateResponse(BaseModel):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    question = models.CharField(max_length=255)
    value = models.DateField()
