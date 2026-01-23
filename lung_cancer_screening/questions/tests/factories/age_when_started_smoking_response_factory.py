import factory

from ..factories.date_of_birth_response_factory import DateOfBirthResponseFactory

from .response_set_factory import ResponseSetFactory
from ...models.age_when_started_smoking_response import AgeWhenStartedSmokingResponse


class AgeWhenStartedSmokingResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AgeWhenStartedSmokingResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Faker('pyint', min_value=15, max_value=50)

    # Create a DateOfBirthResponse linked to the same response_set
    date_of_birth_response = factory.RelatedFactory(
        DateOfBirthResponseFactory,
        factory_related_name="value",
    )
