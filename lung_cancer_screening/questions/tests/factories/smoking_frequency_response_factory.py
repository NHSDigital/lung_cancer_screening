import factory

from ..factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...models.smoking_frequency_response import SmokingFrequencyResponse, SmokingFrequencyValues

class SmokingFrequencyResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SmokingFrequencyResponse

    tobacco_smoking_history = factory.SubFactory(TobaccoSmokingHistoryFactory)
    value =  factory.Iterator(SmokingFrequencyValues)

    class Params:
        daily = factory.Trait(
            value=factory.Iterator(SmokingFrequencyValues.DAILY),
        )
        weekly = factory.Trait(
            value=factory.Iterator(SmokingFrequencyValues.WEEKLY),
        )
        monthly = factory.Trait(
            value=factory.Iterator(SmokingFrequencyValues.MONTHLY),
        )

