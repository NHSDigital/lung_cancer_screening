import factory

from .response_set_factory import ResponseSetFactory
from ...models.cancer_diagnosis_response import CancerDiagnosisResponse


class CancerDiagnosisResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CancerDiagnosisResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Faker('boolean')
