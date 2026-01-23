from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from .base import BaseModel, BaseQuerySet
from .user import User

class ResponseSetQuerySet(BaseQuerySet):
    def unsubmitted(self):
        return self.filter(submitted_at=None)

    def submitted(self):
        return self.filter(submitted_at__isnull=False)

    def recently_submitted(self):
        submitted_since = timezone.now() - relativedelta(days=ResponseSet.RECENTLY_SUBMITTED_PERIOD_DAYS)
        return self.submitted().filter(submitted_at__gte=submitted_since)

class ResponseSet(BaseModel):
    RECENTLY_SUBMITTED_PERIOD_DAYS = 0 if settings.DISABLE_RECENT_SUBMISSION_LIMITATION else 365

    # Query managers
    objects = ResponseSetQuerySet.as_manager()

    # Attributes
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(submitted_at__isnull=True),
                name="unique_unsubmitted_response_per_user",
                violation_error_message="An unsubmitted response set already exists for this user"
            )
        ]

    def clean(self):
        super().clean()
        self._validate_any_submitted_response_set_recently()
        self._validate_complete_on_submission()


    def has_user_submitted_response_set_recently(self):
        return self.user and self.user.has_recently_submitted_responses(excluding=self)


    def _validate_any_submitted_response_set_recently(self):
        if self.has_user_submitted_response_set_recently():
            raise ValidationError(
                "Responses have already been submitted for this user"
            )


    def _validate_complete_on_submission(self):
        if self.submitted_at and not self.is_complete():
            raise ValidationError(
                "Response set must be complete before it can be submitted"
            )


    def _response_attrs(self):
        response_attrs = [
            'asbestos_exposure_response',
            'cancer_diagnosis_response',
            'check_need_appointment_response',
            'date_of_birth_response',
            'education_response',
            'ethnicity_response',
            'family_history_lung_cancer',
            'gender_response',
            'have_you_ever_smoked_response',
            'height_response',
            'respiratory_conditions_response',
            'sex_at_birth_response',
            'weight_response',
        ]

        if hasattr(self, 'family_history_lung_cancer') and self.family_history_lung_cancer.is_truthy():
            response_attrs.append('relatives_age_when_diagnosed')

        return response_attrs


    def is_complete(self):
        return all(hasattr(self, attr) for attr in self._response_attrs())


    def is_eligible(self):
        if not all(
            hasattr(self, attr) for attr in [
                'have_you_ever_smoked_response',
                'date_of_birth_response',
                'check_need_appointment_response'
            ]
        ):
            return False

        return all([
            self.have_you_ever_smoked_response.is_eligible(),
            self.date_of_birth_response.is_eligible(),
            self.check_need_appointment_response.is_eligible()
        ])
