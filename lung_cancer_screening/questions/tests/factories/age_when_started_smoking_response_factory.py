import factory

from ..factories.date_of_birth_response_factory import DateOfBirthResponseFactory

from .response_set_factory import ResponseSetFactory
from ...models.age_when_started_smoking_response import AgeWhenStartedSmokingResponse


class AgeWhenStartedSmokingResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AgeWhenStartedSmokingResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Faker('pyint', min_value=15, max_value=50)

    @factory.post_generation
    def date_of_birth_response(obj, create, extracted, **kwargs):
        """Create a DateOfBirthResponse linked to the same response_set if one doesn't exist."""
        if extracted:
            # Use the provided DateOfBirthResponse
            return extracted

        # Check if response_set already has a date_of_birth_response
        if hasattr(obj.response_set, 'date_of_birth_response'):
            return obj.response_set.date_of_birth_response

        if create:
            # Create a DateOfBirthResponse with the same response_set
            DateOfBirthResponseFactory.create(response_set=obj.response_set, **kwargs)
        else:
            # Build a DateOfBirthResponse with the same response_set
            DateOfBirthResponseFactory.build(response_set=obj.response_set, **kwargs)
