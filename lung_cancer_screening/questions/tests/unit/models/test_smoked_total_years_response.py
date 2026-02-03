from django.test import TestCase, tag
from django.core.exceptions import ValidationError

from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.smoked_total_years_response_factory import SmokedTotalYearsResponseFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory


@tag("SmokedTotalYears")
class TestSmokedTotalYearsResponse(TestCase):
    def setUp(self):
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory()
        self.age_started_smoking_response = AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.tobacco_smoking_history.response_set
        )


    def test_has_a_valid_factory(self):
        model = SmokedTotalYearsResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history
        )
        model.full_clean()


    def test_has_tobacco_smoking_history_as_foreign_key(self):
        response = SmokedTotalYearsResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=10
        )

        self.assertEqual(response.tobacco_smoking_history, self.tobacco_smoking_history)

    def test_has_value_as_int(self):
        response = SmokedTotalYearsResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=10
        )

        self.assertIsInstance(response.value, int)


    def test_is_invalid_if_the_value_is_less_than_0(self):
        response = SmokedTotalYearsResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=0
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn("value", context.exception.message_dict)
        self.assertIn("The number of years you smoked cigarettes must be at least 1", context.exception.message_dict["value"])


    def test_is_invalid_if_there_is_no_age_when_started_smoking_response(self):
        self.age_started_smoking_response.delete()

        response = SmokedTotalYearsResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=1
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn("value", context.exception.message_dict)
        self.assertIn(
            "You must answer age when started smoking before answering how many years you have smoked cigarettes",
            context.exception.message_dict["value"]
        )


    def test_is_invalid_if_the_value_is_greater_than_the_years_smoked_overall(self):
        response = SmokedTotalYearsResponseFactory.build(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=self.age_started_smoking_response.years_smoked_including_stopped() + 1
        )

        with self.assertRaises(ValidationError) as context:
            response.full_clean()

        self.assertIn("value", context.exception.message_dict)
        self.assertIn(
            "The number of years you smoked cigarettes must be fewer than the total number of years you have been smoking",
            context.exception.message_dict["value"]
        )
