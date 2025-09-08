from django.db import models
from .base import BaseModel

class Participant(BaseModel):
    unique_id = models.CharField(max_length=255, unique=True)
