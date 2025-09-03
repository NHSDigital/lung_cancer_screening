from django.db import models
from .base import BaseModel
from django.core.exceptions import ValidationError

class Participant(BaseModel):
    unique_id = models.CharField(max_length=255, unique=True)

    def clean(self):
        super().clean()

        if not self.unique_id:
            raise ValidationError({
                'unique_id': "Participant unique id is required"
            })
