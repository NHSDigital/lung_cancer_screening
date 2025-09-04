from django.db import models
from .base import BaseModel
from .participant import Participant

class BooleanResponse(BaseModel):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    question = models.CharField(max_length=255)
    value = models.BooleanField()
