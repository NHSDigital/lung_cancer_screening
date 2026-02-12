from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, sub, **extra_fields):
        if not sub:
            raise ValueError('The sub must be set')

        user = self.model(sub=sub, **extra_fields)
        # Set an unusable password since AbstractBaseUser requires it
        user.set_unusable_password()
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    sub = models.CharField(max_length=255, unique=True)
    nhs_number = models.CharField(max_length=10, unique=True)
    given_name = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'sub'
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

    def most_recent_response_set(self):
        return self.responseset_set.order_by('-submitted_at').first()

    @property
    def full_name(self):
        return f"{self.given_name} {self.family_name}"
