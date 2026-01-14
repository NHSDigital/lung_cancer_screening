from django.test import TestCase, tag
from datetime import date
from dateutil.relativedelta import relativedelta

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.date_of_birth_response_factory import DateOfBirthResponseFactory

from ....models.date_of_birth_response import DateOfBirthResponse


@tag("DateOfBirth")
class TestDateOfBirthResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = DateOfBirthResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response = DateOfBirthResponse.objects.create(
            response_set=self.response_set,
            value=date(2000, 9, 8)
        )

        self.assertEqual(response.response_set, self.response_set)

    def test_has_value_as_date(self):
        response = DateOfBirthResponse.objects.create(
            response_set=self.response_set,
            value=date(2000, 9, 8)
        )

        self.assertIsInstance(response.value, date)

    def test_is_currently_in_age_range_returns_true_when_in_range(self):
        fifty_five_years_ago = date.today() - relativedelta(years=55)
        response = DateOfBirthResponseFactory.build(
            value=fifty_five_years_ago
        )

        self.assertTrue(response.is_currently_in_age_range())

    def test_is_currently_in_age_range_returns_false_when_too_old(self):
        fifty_five_years_ago = date.today() - relativedelta(years=55)
        response = DateOfBirthResponseFactory.build(
            value=fifty_five_years_ago
        )

        self.assertTrue(response.is_currently_in_age_range())
