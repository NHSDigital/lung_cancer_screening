from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .base import BaseModel
from .response_set import ResponseSet


class HaveYouEverSmokedValues(models.IntegerChoices):
    YES_I_CURRENTLY_SMOKE = 0, 'Yes, I currently smoke'
    YES_I_USED_TO_SMOKE_REGULARLY = 1, 'Yes, I used to smoke'
    YES_BUT_ONLY_A_FEW_TIMES = 2, 'Yes, but I have smoked fewer than 100 cigarettes in my lifetime'
    NO_I_HAVE_NEVER_SMOKED = 3, 'No, I have never smoked'


class HaveYouEverSmokedResponse(BaseModel):
    Values = HaveYouEverSmokedValues

    ELIGIBLE_VALUES = [
        HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY.value,
        HaveYouEverSmokedValues.YES_I_CURRENTLY_SMOKE.value
    ]
    INELIGIBLE_VALUES = [
        HaveYouEverSmokedValues.YES_BUT_ONLY_A_FEW_TIMES.value,
        HaveYouEverSmokedValues.NO_I_HAVE_NEVER_SMOKED.value
    ]

    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='have_you_ever_smoked_response')
    value = models.IntegerField(choices=HaveYouEverSmokedValues.choices)


    def is_eligible(self):
        return self.value in self.ELIGIBLE_VALUES


    def is_current_smoker(self):
        return self.value == HaveYouEverSmokedValues.YES_I_CURRENTLY_SMOKE.value


    def is_former_smoker(self):
        return self.value == HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY.value


@receiver(post_save, sender=HaveYouEverSmokedResponse)
def remove_when_you_quit_smoking_if_not_current(sender, instance, **kwargs):
    if (
        not instance.is_current_smoker()
        and instance.response_set
        and hasattr(instance.response_set, "when_you_quit_smoking_response")
    ):
        instance.response_set.when_you_quit_smoking_response.delete()
