from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ....models.weight_response import WeightResponse


class TestWeightResponse(TestCase):
    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = WeightResponse.objects.create(
            response_set=response_set,
            metric=680
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_metric_as_int(self):
        response_set = ResponseSetFactory()
        response = WeightResponse.objects.create(
            response_set=response_set,
            metric=680
        )

        self.assertIsInstance(response.metric, int)

    def test_has_imperial_as_int(self):
        response_set = ResponseSetFactory()
        response = WeightResponse.objects.create(
            response_set=response_set,
            imperial=140
        )

        self.assertIsInstance(response.imperial, int)
