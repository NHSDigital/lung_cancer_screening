from django.db import models

from .base import BaseModel
from .response_set import ResponseSet

class TermsOfUseResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='terms_of_use_response')
    value = models.BooleanField()

    def has_accepted(self):
        return self.value
