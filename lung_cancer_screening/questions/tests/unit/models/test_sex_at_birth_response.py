from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.sex_at_birth_response_factory import SexAtBirthResponseFactory

from ....models.sex_at_birth_response import SexAtBirthResponse, SexAtBirthValues


@tag("SexAtBirth")
class TestSexAtBirthResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = SexAtBirthResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = SexAtBirthResponse.objects.create(
            response_set=response_set,
            value=SexAtBirthValues.MALE
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_value_as_string(self):
        response_set = ResponseSetFactory()
        response = SexAtBirthResponse.objects.create(
            response_set=response_set,
            value=SexAtBirthValues.MALE
        )

        self.assertIsInstance(response.value, str)
