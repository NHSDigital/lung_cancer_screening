from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ....models.gender_response import GenderResponse, GenderValues


class TestGenderResponse(TestCase):
    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = GenderResponse.objects.create(
            response_set=response_set,
            value=GenderValues.MALE
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_value_as_string(self):
        response_set = ResponseSetFactory()
        response = GenderResponse.objects.create(
            response_set=response_set,
            value=GenderValues.MALE
        )

        self.assertIsInstance(response.value, str)
