from django.db import models
from .base import BaseModel

class Participant(BaseModel):
    unique_id = models.CharField(max_length=255, unique=True)

    def responses(self):
        return list(self.dateresponse_set.all()) + list(self.booleanresponse_set.all())
