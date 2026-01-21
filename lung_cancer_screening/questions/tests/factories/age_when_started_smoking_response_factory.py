import factory

from .response_set_factory import ResponseSetFactory
from ...models.age_when_started_smoking_response import AgeWhenStartedSmokingResponse


class AgeWhenStartedSmokingResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AgeWhenStartedSmokingResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    #response_set = factory.SubFactory(ResponseSetFactory(date_of_birth_response="01-01-1963"))
    #print(f"response_set.date_of_birth_response.value : {response_set.date_of_birth_response.value}")
    value = factory.Faker('pyint', min_value=15, max_value=50)
