import factory

from .response_set_factory import ResponseSetFactory
from ...models.gender_response import GenderResponse, GenderValues


class GenderResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GenderResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Iterator(GenderValues)
