import factory

from .tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...models.smoked_amount_response import SmokedAmountResponse


class SmokedAmountResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SmokedAmountResponse

    tobacco_smoking_history = factory.SubFactory(TobaccoSmokingHistoryFactory)
    value = 20
