import factory

from .response_set_factory import ResponseSetFactory
from ...models.date_of_birth_response import DateOfBirthResponse


class DateOfBirthResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DateOfBirthResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Faker('date_of_birth', minimum_age=10, maximum_age=74)

    class Params:
        eligible = factory.Trait(
            value=factory.Faker('date_of_birth', minimum_age=55, maximum_age=74)
        )

        ineligible = factory.Trait(
            value=factory.Faker('date_of_birth', maximum_age=54)
        )
