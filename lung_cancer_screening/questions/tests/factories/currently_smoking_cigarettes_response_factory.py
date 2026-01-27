import factory

from ...models.currently_smoking_cigarettes_response import CurrentlySmokingCigarettesResponse

from .response_set_factory import ResponseSetFactory


class CurrentlySmokingCigarettesResponseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CurrentlySmokingCigarettesResponse

    response_set = factory.SubFactory(ResponseSetFactory)
    value = factory.Faker('boolean')
