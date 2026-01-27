from django.test import TestCase, tag

from django.utils import timezone
from dateutil.relativedelta import relativedelta

from ....models.age_when_started_smoking_response import AgeWhenStartedSmokingResponse

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.date_of_birth_response_factory import DateOfBirthResponseFactory
from ....forms.age_when_started_smoking_form import AgeWhenStartedSmokingForm
from ...factories.periods_when_you_stopped_smoking_response_factory import PeriodsWhenYouStoppedSmokingResponseFactory
from ....models.periods_when_you_stopped_smoking_response import PeriodsWhenYouStoppedSmokingResponse


@tag("AgeWhenStartedSmoking")
class TestAgeWhenStartedSmokingForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        DateOfBirthResponseFactory(
            response_set=self.response_set,
            value=timezone.now() - relativedelta(years=int(60))
        )
        self.response = AgeWhenStartedSmokingResponse(
            response_set=self.response_set
        )

    def test_is_valid_with_valid_input(self):
        form = AgeWhenStartedSmokingForm(
            instance=self.response,
            data={
                "value": 18
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            18
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = AgeWhenStartedSmokingForm(
            instance=self.response,
            data={
                "value": "invalid"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Enter your age when you started smoking"]
        )

    def test_is_invalid_when_none_is_entered(self):
        form = AgeWhenStartedSmokingForm(
            instance=self.response,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Enter your age when you started smoking"]
        )

    def test_is_invalid_when_zero_is_entered(self):
        form = AgeWhenStartedSmokingForm(
            instance=self.response,
            data={
                "value": 0
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["The age you started smoking must be between 1 and your current age"]
        )

    def test_is_invalid_if_no_date_of_birth(self):
        response_set = ResponseSetFactory()
        response = AgeWhenStartedSmokingResponse(
            response_set=response_set
        )
        form = AgeWhenStartedSmokingForm(
            instance=response,
            data={
                "value": 70
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["<a href=\"/date-of-birth\">Provide your date of birth</a> before answering this question"]
        )

    def test_is_invalid_when_age_entered_greater_than_current_age(self):
        form = AgeWhenStartedSmokingForm(
            instance=self.response,
            data={
                "value": 70
            }
        )

        self.assertFalse(form.is_valid())

        self.assertEqual(
            form.errors["value"],
            ["The age you started smoking must be the same as, or less than your current age"]
        )


    def test_deletes_periods_when_stopped_smoking_response_if_age_started_smoking_is_changed(self):
        self.response.value = 17
        self.response.save()

        PeriodsWhenYouStoppedSmokingResponseFactory.create(
            response_set=self.response_set,
            value=True,
            duration_years=self.response.years_smoked_including_stopped() - 1
        )
        form = AgeWhenStartedSmokingForm(
            instance=self.response,
            data={
                "value": 18
            }
        )
        form.save()

        self.assertFalse(PeriodsWhenYouStoppedSmokingResponse.objects.filter(response_set=self.response_set).exists())


    def test_does_not_delete_periods_when_stopped_smoking_response_if_age_started_smoking_is_not_changed(self):
        self.response.value = 18
        self.response.save()

        PeriodsWhenYouStoppedSmokingResponseFactory.create(
            response_set=self.response_set,
            value=True,
            duration_years=self.response.years_smoked_including_stopped() - 1
        )
        form = AgeWhenStartedSmokingForm(
            instance=self.response,
            data={
                "value": 18
            }
        )
        form.save()

        self.assertTrue(PeriodsWhenYouStoppedSmokingResponse.objects.filter(response_set=self.response_set).exists())
