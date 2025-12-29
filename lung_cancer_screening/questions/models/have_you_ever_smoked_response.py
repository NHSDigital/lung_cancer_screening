from django.db import models

from .base import BaseModel
from .response_set import ResponseSet


class HaveYouEverSmokedValues(models.IntegerChoices):
    YES_I_CURRENTLY_SMOKE = 0, 'Yes, I currently smoke'
    YES_I_USED_TO_SMOKE_REGULARLY = 1, 'Yes, I used to smoke'
    YES_BUT_ONLY_A_FEW_TIMES = 2, 'Yes, but I have smoked fewer than 100 cigarettes in my lifetime'
    NO_I_HAVE_NEVER_SMOKED = 3, 'No, I have never smoked'


class HaveYouEverSmokedResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='have_you_ever_smoked_response')
    value = models.IntegerField(choices=HaveYouEverSmokedValues.choices)
