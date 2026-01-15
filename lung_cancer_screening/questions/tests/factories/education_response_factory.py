import factory

from .response_set_factory import ResponseSetFactory
from ...models.education_response import EducationResponse, EducationValues


class EducationResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EducationResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = [EducationValues.GCSES]
