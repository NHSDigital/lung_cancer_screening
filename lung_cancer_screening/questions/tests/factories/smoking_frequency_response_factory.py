import factory

from ..factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...models.smoking_frequency_response import SmokingFrequencyResponse, SmokingFrequencyValues

class SmokingFrequencyResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SmokingFrequencyResponse

    tobacco_smoking_history = factory.SubFactory(TobaccoSmokingHistoryFactory)
    value =  factory.Iterator(SmokingFrequencyValues)
