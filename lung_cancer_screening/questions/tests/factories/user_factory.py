import factory

from ...models.user import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    sub = factory.Sequence(lambda n: f"nhs-login-sub-{n}")
    nhs_number = factory.Sequence(lambda n: f"9{str(n).zfill(9)}")
    password = factory.django.Password(None)
    email = factory.Faker("email")
    given_name = factory.Faker("first_name")
    family_name = factory.Faker("last_name")
