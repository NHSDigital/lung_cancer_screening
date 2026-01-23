from django.test import TestCase, tag
from django.core.exceptions import ValidationError

from datetime import datetime
from dateutil.relativedelta import relativedelta

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory
from ...factories.date_of_birth_response_factory import DateOfBirthResponseFactory

from ....models.age_when_started_smoking_response import AgeWhenStartedSmokingResponse

@tag("AgeWhenStartedSmoking")
class TestAgeWhenStartedSmokingResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.date_of_birth_response = DateOfBirthResponseFactory(
            response_set=self.response_set,
            value=datetime.now() - relativedelta(years=60)
        )

    def test_has_a_valid_factory(self):
        model = AgeWhenStartedSmokingResponseFactory.build(response_set=self.response_set)
        model.full_clean()

    def test_has_response_set_as_foreign_key(self):
        response = AgeWhenStartedSmokingResponse.objects.create(
            response_set=self.response_set,
            value=17
        )

        self.assertEqual(response.response_set, self.response_set)

    def test_has_value_as_int(self):
        response = AgeWhenStartedSmokingResponse.objects.create(
            response_set=self.response_set,
            value=17
        )

        self.assertIsInstance(response.value, int)

    def test_is_invalid_age_is_greater_than_current_age(self):
        age_when_started_smoking_response = AgeWhenStartedSmokingResponseFactory.build(
            response_set=self.response_set,
            value=self.date_of_birth_response.age_in_years() + 1
        )

        with self.assertRaises(ValidationError) as context:
            age_when_started_smoking_response.full_clean()

        self.assertEqual(
            context.exception.messages[0],
            "age started smoking must be less than current age"
        )
