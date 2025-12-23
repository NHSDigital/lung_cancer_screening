import factory

from .response_set_factory import ResponseSetFactory
from ...models.sex_at_birth_response import SexAtBirthResponse, SexAtBirthValues


class SexAtBirthResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SexAtBirthResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Iterator(SexAtBirthValues)
