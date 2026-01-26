import factory

from .response_set_factory import ResponseSetFactory
from ...models.periods_when_you_stopped_smoking_response import PeriodsWhenYouStoppedSmokingResponse


class PeriodsWhenYouStoppedSmokingResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PeriodsWhenYouStoppedSmokingResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = False
