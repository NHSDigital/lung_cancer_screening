import factory

from .response_set_factory import ResponseSetFactory
from ...models.weight_response import WeightResponse


class WeightResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WeightResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    imperial = None
    metric = factory.Maybe(
        factory.LazyAttribute(lambda obj: obj.imperial is not None),
        factory.LazyAttribute(lambda obj: None),
        factory.Faker('pyint', min_value=WeightResponse.MIN_WEIGHT_METRIC, max_value=WeightResponse.MAX_WEIGHT_METRIC)
    )
