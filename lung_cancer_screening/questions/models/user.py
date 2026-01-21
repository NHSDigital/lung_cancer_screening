from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, nhs_number, **extra_fields):
        if not nhs_number:
            raise ValueError('The NHS number must be set')
        user = self.model(nhs_number=nhs_number, **extra_fields)
        # Set an unusable password since AbstractBaseUser requires it
        user.set_unusable_password()
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    nhs_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'nhs_number'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate before saving
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def has_recently_submitted_responses(self, excluding=None):
        query = self.responseset_set.recently_submitted()

        if excluding:
            query = query.exclude(id=excluding.id)

        return query.exists()
