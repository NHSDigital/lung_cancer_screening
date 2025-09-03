from django.db import models
from .base import BaseModel
from .participant import Participant

class QuestionnaireResponse(BaseModel):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    value = models.DateField()
