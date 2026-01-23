import factory

from .response_set_factory import ResponseSetFactory
from ...models.check_need_appointment_response import CheckNeedAppointmentResponse


class CheckNeedAppointmentResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CheckNeedAppointmentResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Faker('boolean')

    class Params:
        eligible = factory.Trait(
            value=False
        )

        ineligible = factory.Trait(
            value=True
        )
