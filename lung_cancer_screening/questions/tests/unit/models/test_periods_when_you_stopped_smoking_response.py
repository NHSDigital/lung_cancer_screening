from django.test import TestCase, tag
from django.core.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.periods_when_you_stopped_smoking_response_factory import PeriodsWhenYouStoppedSmokingResponseFactory
from ...factories.date_of_birth_response_factory import DateOfBirthResponseFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory
from ....models.periods_when_you_stopped_smoking_response import PeriodsWhenYouStoppedSmokingResponse



@tag("PeriodsWhenYouStoppedSmoking")
class TestPeriodsWhenYouStoppedSmokingResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

        # Following responses required by validator
        self.date_of_birth_response = DateOfBirthResponseFactory.create(response_set=self.response_set)
        self.age_when_started_smoking_response = AgeWhenStartedSmokingResponseFactory.create(response_set=self.response_set)


    def test_has_a_valid_factory(self):
        model = PeriodsWhenYouStoppedSmokingResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response = PeriodsWhenYouStoppedSmokingResponseFactory.build(
            response_set=self.response_set, value=True
        )

        self.assertEqual(response.response_set, self.response_set)

    def test_has_value_as_bool(self):
        response = PeriodsWhenYouStoppedSmokingResponseFactory.build(
            response_set=self.response_set, value=False
        )

        self.assertIsInstance(response.value, bool)


    def test_has_duration_years_as_integer(self):
        response = PeriodsWhenYouStoppedSmokingResponseFactory.build(
            response_set=self.response_set,
            value=True,
            duration_years=10
        )

        self.assertIsInstance(response.duration_years, int)


    def test_is_invalid_if_duration_years_not_set_and_value_is_true(self):
        response = PeriodsWhenYouStoppedSmokingResponse(
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


    def test_is_valid_if_duration_years_is_set_and_value_is_true(self):
        response = PeriodsWhenYouStoppedSmokingResponse(
            response_set=self.response_set,
            value=True,
            duration_years=self.age_when_started_smoking_response.years_smoked_including_stopped() - 1
        )

        response.full_clean()


    def test_is_valid_if_duration_years_not_set_and_value_is_false(self):
        response = PeriodsWhenYouStoppedSmokingResponse(
            response_set=self.response_set,
            value=False,
            duration_years=None
        )

        response.full_clean()


    def test_is_invalid_if_they_havent_answered_age_started_smoking(self):
        self.response_set.age_when_started_smoking_response.delete()
        self.response_set.refresh_from_db()

        response = PeriodsWhenYouStoppedSmokingResponse(
            response_set=self.response_set,
            value=True,
            duration_years=10
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertEqual(
            context.exception.messages[0],
            "age started smoking not set",
        )


    def test_is_invalid_if_duration_years_is_longer_than_time_they_have_smoked(self):
        self.date_of_birth_response.value = datetime.today() - relativedelta(years=55)
        self.date_of_birth_response.save()
        self.age_when_started_smoking_response.value = 18
        self.age_when_started_smoking_response.save()

        response = PeriodsWhenYouStoppedSmokingResponseFactory.build(
            response_set=self.response_set,
            value=True,
            duration_years=self.date_of_birth_response.age_in_years() - self.age_when_started_smoking_response.value + 1
        )
        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertEqual(
            context.exception.messages[0],
            "The number of years you stopped smoking must be fewer than the total number of years you have been smoking",
        )
