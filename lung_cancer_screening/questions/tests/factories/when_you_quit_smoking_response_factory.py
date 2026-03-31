import factory

from .response_set_factory import ResponseSetFactory
from ...models.when_you_quit_smoking_response import WhenYouQuitSmokingResponse


class WhenYouQuitSmokingResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WhenYouQuitSmokingResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Faker("pyint", min_value=18, max_value=100)
