from django.db import models

from .base import BaseModel
from .response_set import ResponseSet


class CheckNeedAppointmentResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='check_need_appointment_response')
    value = models.BooleanField()

    def is_eligible(self):
        return not self.value
