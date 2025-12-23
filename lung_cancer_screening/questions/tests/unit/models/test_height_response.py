from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.height_response_factory import HeightResponseFactory

from ....models.height_response import HeightResponse


class TestHeightResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = HeightResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = HeightResponse.objects.create(
            response_set=response_set,
            metric=1700
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_metric_as_int(self):
        response_set = ResponseSetFactory()
        response = HeightResponse.objects.create(
            response_set=response_set,
            metric=1700
        )

        self.assertIsInstance(response.metric, int)

    def test_has_imperial_as_int(self):
        response_set = ResponseSetFactory()
        response = HeightResponse.objects.create(
            response_set=response_set,
            imperial=68
        )

        self.assertIsInstance(response.imperial, int)
