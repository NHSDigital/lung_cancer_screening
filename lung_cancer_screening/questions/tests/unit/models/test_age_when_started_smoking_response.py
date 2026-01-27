from django.test import TestCase, tag
from django.core.exceptions import ValidationError

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory
from ...factories.date_of_birth_response_factory import DateOfBirthResponseFactory

from ....models.age_when_started_smoking_response import AgeWhenStartedSmokingResponse

@tag("AgeWhenStartedSmoking","wip")
class TestAgeWhenStartedSmokingResponse(TestCase):
    def test_has_a_valid_factory(self):
        model = AgeWhenStartedSmokingResponseFactory.build()
        model.full_clean()

    def test_has_response_set_as_foreign_key(self):
        response = AgeWhenStartedSmokingResponse.objects.create(
            response_set=ResponseSetFactory(),
            value=17
        )

        self.assertEqual(response.response_set, response.response_set)
    def test_has_value_as_int(self):
        response = AgeWhenStartedSmokingResponse.objects.create(
            response_set=ResponseSetFactory(),
            value=17
        )

        self.assertIsInstance(response.value, int)

    def test_is_invalid_age_is_greater_than_current_age(self):
        age_when_started_smoking_response = AgeWhenStartedSmokingResponseFactory.build(
            response_set=ResponseSetFactory(),
            value=DateOfBirthResponseFactory().age_in_years() + 1
        )

        with self.assertRaises(ValidationError) as context:
            age_when_started_smoking_response.full_clean()

        self.assertEqual(
            context.exception.messages[0],
            "age started smoking must be less than current age"
        )
