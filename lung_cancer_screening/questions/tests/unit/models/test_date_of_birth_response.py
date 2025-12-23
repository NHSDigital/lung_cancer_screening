from django.test import TestCase
from datetime import date

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.date_of_birth_response_factory import DateOfBirthResponseFactory

from ....models.date_of_birth_response import DateOfBirthResponse


class TestDateOfBirthResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = DateOfBirthResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = DateOfBirthResponse.objects.create(
            response_set=response_set,
            value=date(2000, 9, 8)
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_value_as_date(self):
        response_set = ResponseSetFactory()
        response = DateOfBirthResponse.objects.create(
            response_set=response_set,
            value=date(2000, 9, 8)
        )

        self.assertIsInstance(response.value, date)
