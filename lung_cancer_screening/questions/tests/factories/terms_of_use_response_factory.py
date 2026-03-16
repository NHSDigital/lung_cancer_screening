import factory

from .response_set_factory import ResponseSetFactory
from ...models.terms_of_use_response import TermsOfUseResponse


class TermsOfUseResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TermsOfUseResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Faker('boolean')

    class Params:
        accepted = factory.Trait(
            value=True
        )

        not_accepted = factory.Trait(
            value=False
        )
