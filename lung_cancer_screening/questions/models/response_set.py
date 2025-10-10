from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from .base import BaseModel
from .participant import Participant

class HaveYouEverSmokedValues(models.IntegerChoices):
    YES_I_CURRENTLY_SMOKE = 0, 'Yes, I currently smoke'
    YES_I_USED_TO_SMOKE_REGULARLY = 1, 'Yes, I used to smoke regularly'
    YES_BUT_ONLY_A_FEW_TIMES = 2, 'Yes, but only a few times'
    NO_I_HAVE_NEVER_SMOKED = 3, 'No, I have never smoked'

class ResponseSet(BaseModel):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    have_you_ever_smoked = models.IntegerField(
        choices=HaveYouEverSmokedValues.choices,
        null=True,
        blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)

    height = models.PositiveIntegerField(null=True, blank=True, validators=[
        MinValueValidator(1397, message="Height must be between 139.7cm and 243.8 cm"),
        MaxValueValidator(2438, message="Height must be between 139.7cm and 243.8 cm"),
    ])

    #height_type

    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["participant"],
                condition=models.Q(submitted_at__isnull=True),
                name="unique_unsubmitted_response_per_participant",
                violation_error_message="An unsubmitted response set already exists for this participant"
            )
        ]

    def clean(self):
        super().clean()

        one_year_ago = timezone.now() - relativedelta(years=1)
        submitted_response_sets_in_last_year = self.participant.responseset_set.filter(submitted_at__gte=one_year_ago)

        if submitted_response_sets_in_last_year:
            raise ValidationError(
                "Responses have already been submitted for this participant"
            )
        
    @property
    def height(self):
        return self.height

    @height.setter
    def _height(self, value):
        if value > 0 :
            print("The date chosen was in the future.")
        self._height = value
