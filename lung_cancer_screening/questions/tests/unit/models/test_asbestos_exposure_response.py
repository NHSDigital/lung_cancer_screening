from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ....models.asbestos_exposure_response import AsbestosExposureResponse


class TestAsbestosExposureResponse(TestCase):
    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = AsbestosExposureResponse.objects.create(
            response_set=response_set,
            value=True
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_value_as_bool(self):
        response_set = ResponseSetFactory()
        response = AsbestosExposureResponse.objects.create(
            response_set=response_set,
            value=False
        )

        self.assertIsInstance(response.value, bool)
