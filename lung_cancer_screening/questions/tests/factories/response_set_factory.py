import factory

from .user_factory import UserFactory
from ...models.response_set import ResponseSet


class ResponseSetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResponseSet

    user = factory.SubFactory(UserFactory)
