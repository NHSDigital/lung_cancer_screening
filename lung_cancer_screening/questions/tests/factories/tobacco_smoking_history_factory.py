import factory

from .response_set_factory import ResponseSetFactory
from ...models.tobacco_smoking_history import (
    TobaccoSmokingHistory,
    TobaccoSmokingHistoryTypes,
)


class TobaccoSmokingHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TobaccoSmokingHistory

    response_set = factory.SubFactory(ResponseSetFactory)
    type = TobaccoSmokingHistoryTypes.CIGARETTES
