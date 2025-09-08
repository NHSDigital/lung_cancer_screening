from django.db import models
from .base import BaseModel
from .participant import Participant

class HaveYouEverSmokedValues(models.IntegerChoices):
    YES_I_CURRENTLY_SMOKE = 0, 'Yes, I currently smoke'
    YES_I_USED_TO_SMOKE_REGULARLY = 1, 'Yes, I used to smoke regularly'
    YES_BUT_ONLY_A_FEW_TIMES = 2, 'Yes, but only a few times'
    NO_I_HAVE_NEVER_SMOKED = 3, 'No, I have never smoked'

class ResponseSet(BaseModel):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    have_you_ever_smoked = models.IntegerField(choices=HaveYouEverSmokedValues.choices, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
