from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .base import BaseModel
from .response_set import ResponseSet


class FamilyHistoryLungCancerValues(models.TextChoices):
    YES = "Y", "Yes"
    NO = "N", "No"
    UNKNOWN = "U", "I do not know"

class FamilyHistoryLungCancerResponse(BaseModel):
    response_set = models.OneToOneField(ResponseSet, on_delete=models.CASCADE, related_name='family_history_lung_cancer')
    value = models.CharField(max_length=1, choices=FamilyHistoryLungCancerValues.choices)


@receiver(post_save, sender=FamilyHistoryLungCancerResponse)
def remove_relatives_age_when_diagnosed_if_not_yes(sender, instance, **kwargs):
    if (
        instance.value != FamilyHistoryLungCancerValues.YES
        and instance.response_set
        and hasattr(instance.response_set, "relatives_age_when_diagnosed")
    ):
        instance.response_set.relatives_age_when_diagnosed.delete()
