from django.db import models
from lung_cancer_screening.services.metrics import Metrics
import logging

logger = logging.getLogger(__name__)

class BaseQuerySet(models.QuerySet):
    def get_or_build(self, **kwargs):
        """
        Get an existing object matching the kwargs, or build a new unsaved instance.
        Returns a tuple of (object, created) where created is True if a new instance was built.
        """
        # Check if any kwargs are unsaved model instances
        for _, value in kwargs.items():
            if isinstance(value, models.Model) and value.pk is None:
                # If we have an unsaved instance, just build a new one
                return (self.model(**kwargs), True)

        try:
            return (self.get(**kwargs), False)
        except self.model.DoesNotExist:
            return (self.model(**kwargs), True)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BaseQuerySet.as_manager()

    @property
    def model_name(self) -> str:
        return self._meta.label_lower

    def save(self, *args, **kwargs):
        is_create = self.pk is None

        old_status = None
        if not is_create and hasattr(self, "status"):
            old_status = (
                self.__class__.objects.filter(pk=self.pk)
                .values_list("status", flat=True)
                .first()
            )


        self.full_clean()  # Validate before saving
        super().save(*args, **kwargs)

        metrics = Metrics()

        if is_create:
            metrics.record_request_created(self.model_name)

        if hasattr(self, "status") and self.status == "submitted" and old_status != "submitted":
            metrics.record_request_submitted(self.model_name)
