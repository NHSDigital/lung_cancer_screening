from django.db import models


class BaseQuerySet(models.QuerySet):
    def get_or_build(self, **kwargs):
        """
        Get an existing object matching the kwargs, or build a new unsaved instance.
        Returns a tuple of (object, created) where created is True if a new instance was built.
        """
        # Check if any kwargs are unsaved model instances
        for key, value in kwargs.items():
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

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate before saving
        super().save(*args, **kwargs)
