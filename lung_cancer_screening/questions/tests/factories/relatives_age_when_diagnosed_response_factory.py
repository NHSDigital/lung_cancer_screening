import factory

from .response_set_factory import ResponseSetFactory
from ...models.relatives_age_when_diagnosed_response import RelativesAgeWhenDiagnosedResponse, RelativesAgeWhenDiagnosedValues


class RelativesAgeWhenDiagnosedResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RelativesAgeWhenDiagnosedResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Iterator(RelativesAgeWhenDiagnosedValues)
