import factory

from .response_set_factory import ResponseSetFactory
from ...models.respiratory_conditions_response import RespiratoryConditionsResponse, RespiratoryConditionValues


class RespiratoryConditionsResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RespiratoryConditionsResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = [RespiratoryConditionValues.COPD]
