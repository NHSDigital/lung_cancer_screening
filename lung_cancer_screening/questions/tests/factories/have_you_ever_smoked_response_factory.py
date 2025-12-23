import factory

from .response_set_factory import ResponseSetFactory
from ...models.have_you_ever_smoked_response import HaveYouEverSmokedResponse, HaveYouEverSmokedValues


class HaveYouEverSmokedResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HaveYouEverSmokedResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Iterator(HaveYouEverSmokedValues)
