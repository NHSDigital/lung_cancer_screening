import factory

from .tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory

from ...models import SmokingCurrentResponse


class SmokingCurrentResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SmokingCurrentResponse

    tobacco_smoking_history = factory.SubFactory(TobaccoSmokingHistoryFactory)
    value = factory.Faker('boolean')
