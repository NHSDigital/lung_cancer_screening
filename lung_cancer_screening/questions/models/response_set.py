from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from decimal import Decimal

from .base import BaseModel
from .participant import Participant

class HaveYouEverSmokedValues(models.IntegerChoices):
    YES_I_CURRENTLY_SMOKE = 0, 'Yes, I currently smoke'
    YES_I_USED_TO_SMOKE_REGULARLY = 1, 'Yes, I used to smoke regularly'
    YES_BUT_ONLY_A_FEW_TIMES = 2, 'Yes, but only a few times'
    NO_I_HAVE_NEVER_SMOKED = 3, 'No, I have never smoked'

class SexAtBirthValues(models.TextChoices):
    FEMALE = "F", 'Female'
    MALE = "M", 'Male'

class GenderValues(models.TextChoices):
    FEMALE = "F", 'Female'
    MALE = "M", 'Male'
    NON_BINARY = "N", 'Non-binary'
    PREFER_NOT_TO_SAY = "P", 'Prefer not to say'
    GP = "G", 'How I describe myself may not match my GP record'

class EthnicityValues(models.TextChoices):
    ASIAN = "A", "Asian or Asian British"
    BLACK = "B", "Black, African, Caribbean or Black British"
    MIXED = "M", "Mixed or multiple ethnic groups"
    WHITE = "W", "White"
    OTHER = "O", "Other ethnic group"
    PREFER_NOT_TO_SAY = "N", "I'd prefer not to say"

class RespiratoryConditionValues(models.TextChoices):
    PNEUMONIA = "P", "Pneumonia"
    EMPHYSEMA = "E", "Emphysema"
    BRONCHITIS = "B", "Chronic bronchitis"
    TUBERCULOSIS = "T", "Tuberculosis (TB)"
    COPD = "C", "Chronic obstructive pulmonary disease (COPD)"
    NONE = "N", "None of the above"

class ResponseSet(BaseModel):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    have_you_ever_smoked = models.IntegerField(
        choices=HaveYouEverSmokedValues.choices,
        null=True,
        blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)

    MAX_HEIGHT_METRIC = 2438
    MIN_HEIGHT_METRIC = 1397
    MAX_HEIGHT_IMPERIAL = 96
    MIN_HEIGHT_IMPERIAL = 55
    height = models.PositiveIntegerField(null=True, blank=True, validators=[
        MinValueValidator(MIN_HEIGHT_METRIC, message="Height must be between 139.7cm and 243.8 cm"),
        MaxValueValidator(MAX_HEIGHT_METRIC, message="Height must be between 139.7cm and 243.8 cm"),
    ])
    height_imperial = models.PositiveIntegerField(null=True, blank=True, validators=[
        MinValueValidator(
            MIN_HEIGHT_IMPERIAL, message="Height must be between 4 feet 7 inches and 8 feet"),
        MaxValueValidator(
            MAX_HEIGHT_IMPERIAL, message="Height must be between 4 feet 7 inches and 8 feet"),
    ])

    MIN_WEIGHT_METRIC = 254
    MAX_WEIGHT_METRIC = 3175
    MAX_WEIGHT_IMPERIAL = 700
    MIN_WEIGHT_IMPERIAL = 56

    weight_metric = models.PositiveIntegerField(null=True, blank=True, validators=[
        MinValueValidator(MIN_WEIGHT_METRIC, message="Weight must be between 25.4kg and 317.5kg"),
        MaxValueValidator(MAX_WEIGHT_METRIC, message="Weight must be between 25.4kg and 317.5kg"),
    ])
    weight_imperial = models.PositiveIntegerField(null=True, blank=True, validators=[
        MinValueValidator(
            MIN_WEIGHT_IMPERIAL, message="Weight must be between 4 stone and 50 stone"),
        MaxValueValidator(
            MAX_WEIGHT_IMPERIAL, message="Weight must be between 4 stone and 50 stone"),
    ])

    sex_at_birth = models.CharField(
        max_length=1,
        choices=SexAtBirthValues.choices,
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=1,
        choices=GenderValues.choices,
        null=True,
        blank=True
    )

    ethnicity = models.CharField(
        max_length=1,
        choices=EthnicityValues.choices,
        null=True,
        blank=True
    )

    respiratory_conditions = ArrayField(
        models.CharField(max_length=1, choices=RespiratoryConditionValues.choices),
        null=True,
        blank=True
    )

    asbestos_exposure = models.BooleanField(
        null=True,
        blank=True
    )

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
    def formatted_height(self):
        if self.height:
            return f"{Decimal(self.height) / 10}cm"
        elif self.height_imperial:
            value = Decimal(self.height_imperial)
            return f"{value // 12} feet {value % 12} inches"

    @property
    def formatted_weight(self):
        if self.weight_metric:
            return f"{Decimal(self.weight_metric) / 10}kg"
        elif self.weight_imperial:
            value = Decimal(self.weight_imperial)
            return f"{value // 14} stone {value % 14} pounds"


