from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.ethnicity_response_factory import EthnicityResponseFactory

from ....models.ethnicity_response import EthnicityResponse, EthnicityValues


class TestEthnicityResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = EthnicityResponseFactory.build(response_set=self.response_set)
        model.full_clean()

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
