from django.test import TestCase, tag
from django.core.exceptions import ValidationError

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.periods_when_you_stopped_smoking_response_factory import PeriodsWhenYouStoppedSmokingResponseFactory



@tag("PeriodsWhenYouStoppedSmoking")
class TestPeriodsWhenYouStoppedSmokingResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = PeriodsWhenYouStoppedSmokingResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response = PeriodsWhenYouStoppedSmokingResponseFactory.create(
            response_set=self.response_set, value=True
        )

        self.assertEqual(response.response_set, self.response_set)

    def test_has_value_as_bool(self):
        response = PeriodsWhenYouStoppedSmokingResponseFactory.create(
            response_set=self.response_set, value=False
        )

        self.assertIsInstance(response.value, bool)

    def test_has_duration_years_as_integer(self):
        response = PeriodsWhenYouStoppedSmokingResponseFactory.create(
            response_set=self.response_set, value=True, duration_years=10
        )

        self.assertIsInstance(response.duration_years, int)


    def test_is_invalid_if_duration_years_not_set_and_value_is_true(self):
        response = PeriodsWhenYouStoppedSmokingResponseFactory.build(
            response_set=self.response_set,
            value=True,
            duration_years=None
        )
        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertEqual(
            context.exception.messages[0],
            "Enter the total number of years you stopped smoking for"
        )
