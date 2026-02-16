from django.test import TestCase, tag
from django.core.exceptions import ValidationError

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.height_response_factory import HeightResponseFactory

from ....models.height_response import HeightResponse


@tag("Height")
class TestHeightResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = HeightResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response = HeightResponseFactory.build(
            response_set=self.response_set,
            metric=1700
        )

        self.assertEqual(response.response_set, self.response_set)


    def test_has_metric_as_int(self):
        response = HeightResponseFactory.build(
            response_set=self.response_set,
            metric=1700
        )

        self.assertIsInstance(response.metric, int)

    def test_has_imperial_as_int(self):
        response = HeightResponseFactory.build(
            response_set=self.response_set,
            imperial=68
        )

        self.assertIsInstance(response.imperial, int)


    def test_is_invalid_if_neither_metric_nor_imperial_are_set(self):
        response = HeightResponseFactory.build(
            response_set=self.response_set,
            metric=None,
            imperial=None
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn(
            "Either metric or imperial height must be provided.",
            context.exception.messages,
        )


    def test_is_invalid_if_both_metric_and_imperial_are_set(self):
        response = HeightResponseFactory.build(
            response_set=self.response_set,
            metric=1700,
            imperial=68
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn(
            "Cannot provide both metric and imperial height.",
            context.exception.messages,
        )


    def test_is_invalid_if_metric_is_less_than_minimum_height(self):
        response = HeightResponseFactory.build(
            response_set=self.response_set,
            metric=HeightResponse.MIN_HEIGHT_METRIC - 1
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn(
            "Height must be between 139.7cm and 243.8 cm",
            context.exception.messages,
        )


    def test_is_invalid_if_metric_is_greater_than_maximum_height(self):
        response = HeightResponseFactory.build(
            response_set=self.response_set,
            metric=HeightResponse.MAX_HEIGHT_METRIC + 1
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn(
            "Height must be between 139.7cm and 243.8 cm",
            context.exception.messages,
        )


    def test_is_invalid_if_imperial_is_less_than_minimum_height(self):
        response = HeightResponseFactory.build(
            response_set=self.response_set,
            imperial=HeightResponse.MIN_HEIGHT_IMPERIAL - 1
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn(
            "Height must be between 4 feet 7 inches and 8 feet",
            context.exception.messages,
        )


    def test_is_invalid_if_imperial_is_greater_than_maximum_height(self):
        response = HeightResponseFactory.build(
            response_set=self.response_set,
            imperial=HeightResponse.MAX_HEIGHT_IMPERIAL + 1
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn(
            "Height must be between 4 feet 7 inches and 8 feet",
            context.exception.messages,
        )
