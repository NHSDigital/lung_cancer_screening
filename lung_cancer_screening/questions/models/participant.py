from django.db import models
from .base import BaseModel

class Participant(BaseModel):
    unique_id = models.CharField(max_length=255, unique=True)

    def unsubmitted_response_sets(self):
        return self.responseset_set.filter(submitted_at__isnull=True)

    def has_unsubmitted_response_set(self):
        return self.unsubmitted_response_sets().exists()
