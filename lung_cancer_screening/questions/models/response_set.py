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


    def has_user_submitted_response_set_recently(self):
        return self.user and self.user.has_recently_submitted_responses()


    def _validate_any_submitted_response_set_recently(self):
        if self.has_user_submitted_response_set_recently():
            raise ValidationError(
                "Responses have already been submitted for this user"
            )
