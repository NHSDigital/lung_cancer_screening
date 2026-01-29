import factory

from .tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...models.smoked_total_years_response import SmokedTotalYearsResponse


class SmokedTotalYearsResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SmokedTotalYearsResponse

    tobacco_smoking_history = factory.SubFactory(TobaccoSmokingHistoryFactory)
    value = 10
