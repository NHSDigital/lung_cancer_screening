import factory
import random

from .response_set_factory import ResponseSetFactory
from ...models.age_when_started_smoking_response import AgeWhenStartedSmokingResponse


def calculate_value(instance):
    if not hasattr(instance.response_set, 'date_of_birth_response'):
        return None
    return random.randint(1, instance.response_set.date_of_birth_response.age_in_years())


class AgeWhenStartedSmokingResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AgeWhenStartedSmokingResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.LazyAttribute(calculate_value)

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        """Ensure date_of_birth_response exists before validation."""
        instance = super()._build(model_class, *args, **kwargs)
        if not hasattr(instance.response_set, 'date_of_birth_response'):
            from ..factories.date_of_birth_response_factory import DateOfBirthResponseFactory
            DateOfBirthResponseFactory.create(response_set=instance.response_set)
            instance.response_set.refresh_from_db()
            if instance.value is None:
                instance.value = random.randint(1, instance.response_set.date_of_birth_response.age_in_years())
        return instance

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Ensure date_of_birth_response exists before save/validation."""
        instance = cls._build(model_class, *args, **kwargs)
        instance.save()
        return instance
