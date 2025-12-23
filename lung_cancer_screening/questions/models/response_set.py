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

    def submitted_in_last_year(self):
        return self.submitted().filter(submitted_at__gte=timezone.now() - relativedelta(years=1))

class ResponseSet(BaseModel):
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

        one_year_ago = timezone.now() - relativedelta(years=1)
        submitted_response_sets_in_last_year = self.user and self.user.responseset_set.filter(submitted_at__gte=one_year_ago)

        if submitted_response_sets_in_last_year:
            raise ValidationError(
                "Responses have already been submitted for this user"
            )


