import factory

from ...models.user import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    nhs_number = factory.Sequence(lambda n: f"9{str(n).zfill(9)}")
    password = factory.django.Password(None)
