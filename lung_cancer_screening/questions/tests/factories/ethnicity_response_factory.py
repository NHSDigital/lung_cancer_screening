import factory

from .response_set_factory import ResponseSetFactory
from ...models.ethnicity_response import EthnicityResponse, EthnicityValues


class EthnicityResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EthnicityResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Iterator(EthnicityValues)
