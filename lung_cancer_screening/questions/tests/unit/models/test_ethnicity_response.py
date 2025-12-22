from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ....models.ethnicity_response import EthnicityResponse, EthnicityValues


class TestEthnicityResponse(TestCase):
    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = EthnicityResponse.objects.create(
            response_set=response_set,
            value=EthnicityValues.WHITE
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_value_as_string(self):
        response_set = ResponseSetFactory()
        response = EthnicityResponse.objects.create(
            response_set=response_set,
            value=EthnicityValues.WHITE
        )

        self.assertIsInstance(response.value, str)
