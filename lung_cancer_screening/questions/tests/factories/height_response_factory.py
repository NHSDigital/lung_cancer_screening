import factory

from .response_set_factory import ResponseSetFactory
from ...models.height_response import HeightResponse


class HeightResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HeightResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    imperial = None
    metric = factory.Maybe(
        factory.LazyAttribute(lambda obj: obj.imperial is not None),
        factory.LazyAttribute(lambda obj: None),
        factory.Faker('pyint', min_value=HeightResponse.MIN_HEIGHT_METRIC, max_value=HeightResponse.MAX_HEIGHT_METRIC)
    )
