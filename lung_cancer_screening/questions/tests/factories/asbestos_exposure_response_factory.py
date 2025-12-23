import factory

from .response_set_factory import ResponseSetFactory
from ...models.asbestos_exposure_response import AsbestosExposureResponse


class AsbestosExposureResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AsbestosExposureResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Faker('boolean')
