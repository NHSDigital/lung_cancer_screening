from django.test import TestCase, tag
from django.core.exceptions import ValidationError

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.date_of_birth_response_factory import DateOfBirthResponseFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory
from ...factories.when_you_quit_smoking_response_factory import WhenYouQuitSmokingResponseFactory

from ....models.when_you_quit_smoking_response import WhenYouQuitSmokingResponse


@tag("WhenYouQuitSmoking")
class TestWhenYouQuitSmokingResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.date_of_birth_response = DateOfBirthResponseFactory(
            response_set=self.response_set,
            eligible=True
        )
        self.age_when_started_smoking_response = AgeWhenStartedSmokingResponseFactory(
            response_set=self.response_set,
            value=self.date_of_birth_response.age_in_years() - 20,
        )


    def test_has_a_valid_factory(self):
        model = WhenYouQuitSmokingResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response = WhenYouQuitSmokingResponse.objects.create(
            response_set=self.response_set,
            value=18
        )

        self.assertEqual(response.response_set, self.response_set)


    def test_is_invalid_date_of_birth_is_unanswered(self):
        self.response_set.date_of_birth_response.delete()
        self.response_set.refresh_from_db()
        response = WhenYouQuitSmokingResponseFactory.build(
            response_set=self.response_set,
            value=18
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertEqual(
            context.exception.message_dict["value"],
            ["date of birth not set"]
        )


    def test_is_invalid_if_age_started_smoking_is_unanswered(self):
        self.age_when_started_smoking_response.delete()
        self.response_set.refresh_from_db()

        response = WhenYouQuitSmokingResponseFactory.build(
            response_set=self.response_set,
            value=18
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertEqual(
            context.exception.message_dict["value"],
            ["age started smoking not set"]
        )
