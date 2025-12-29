from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.weight_response_factory import WeightResponseFactory

from ....models.weight_response import WeightResponse


class TestWeightResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()


    def test_has_a_valid_factory(self):
        model = WeightResponseFactory.build(response_set=self.response_set)
        model.full_clean()


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
