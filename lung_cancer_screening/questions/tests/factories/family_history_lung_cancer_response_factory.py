import factory

from .response_set_factory import ResponseSetFactory
from ...models.family_history_lung_cancer_response import FamilyHistoryLungCancerResponse, FamilyHistoryLungCancerValues


class FamilyHistoryLungCancerResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FamilyHistoryLungCancerResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Iterator(FamilyHistoryLungCancerValues)
