from django.test import TestCase, tag
from django.core.exceptions import ValidationError

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.weight_response_factory import WeightResponseFactory

from ....models.weight_response import WeightResponse


@tag("Weight")
class TestWeightResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()


    def test_has_a_valid_factory(self):
        model = WeightResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response = WeightResponse.objects.create(
            response_set=self.response_set,
            metric=680
        )

        self.assertEqual(response.response_set, self.response_set)


    def test_has_metric_as_int(self):
        response = WeightResponse.objects.create(
            response_set=self.response_set,
            metric=680
        )

        self.assertIsInstance(response.metric, int)


    def test_has_imperial_as_int(self):
        response = WeightResponse.objects.create(
            response_set=self.response_set,
            imperial=140
        )

        self.assertIsInstance(response.imperial, int)


    def test_is_invalid_if_neither_metric_nor_imperial_are_set(self):
        response = WeightResponseFactory.build(
            response_set=self.response_set,
            metric=None,
            imperial=None
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn(
            "Either metric or imperial weight must be provided.",
            context.exception.messages,
        )


    def test_is_invalid_if_both_metric_and_imperial_are_set(self):
        response = WeightResponseFactory.build(
            response_set=self.response_set,
            metric=1700,
            imperial=68
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn(
            "Cannot provide both metric and imperial weight.",
            context.exception.messages,
        )


    def test_is_invalid_if_metric_is_less_than_minimum_weight(self):
        response = WeightResponseFactory.build(
            response_set=self.response_set,
            metric=WeightResponse.MIN_WEIGHT_METRIC - 1
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn(
            "Weight must be between 25.4kg and 317.5kg",
            context.exception.messages,
        )


    def test_is_invalid_if_metric_is_greater_than_maximum_weight(self):
        response = WeightResponseFactory.build(
            response_set=self.response_set,
            metric=WeightResponse.MAX_WEIGHT_METRIC + 1
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn(
            "Weight must be between 25.4kg and 317.5kg",
            context.exception.messages,
        )


    def test_is_invalid_if_imperial_is_less_than_minimum_weight(self):
        response = WeightResponseFactory.build(
            response_set=self.response_set,
            imperial=WeightResponse.MIN_WEIGHT_IMPERIAL - 1
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn(
            "Weight must be between 4 stone and 50 stone",
            context.exception.messages,
        )


    def test_is_invalid_if_imperial_is_greater_than_maximum_weight(self):
        response = WeightResponseFactory.build(
            response_set=self.response_set,
            imperial=WeightResponse.MAX_WEIGHT_IMPERIAL + 1
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn(
            "Weight must be between 4 stone and 50 stone",
            context.exception.messages,
        )
