import factory

from .response_set_factory import ResponseSetFactory
from ...models.date_of_birth_response import DateOfBirthResponse


class DateOfBirthResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DateOfBirthResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Faker('date_of_birth')
