from django.test import TestCase, tag

from lung_cancer_screening.questions.tests.factories.have_you_ever_smoked_response_factory import HaveYouEverSmokedResponseFactory

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.date_of_birth_response_factory import DateOfBirthResponseFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory
from ...factories.when_you_quit_smoking_response_factory import WhenYouQuitSmokingResponseFactory
from ...factories.periods_when_you_stopped_smoking_response_factory import PeriodsWhenYouStoppedSmokingResponseFactory

from ....forms.when_you_quit_smoking_form import WhenYouQuitSmokingForm
from ....forms.age_when_started_smoking_form import AgeWhenStartedSmokingForm

from ....models.periods_when_you_stopped_smoking_response import PeriodsWhenYouStoppedSmokingResponse
from ....models.when_you_quit_smoking_response import WhenYouQuitSmokingResponse


@tag("WhenYouQuitSmoking")
class TestWhenYouQuitSmokingForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

        HaveYouEverSmokedResponseFactory(response_set=self.response_set, current_smoker=True)

        self.date_of_birth_response = DateOfBirthResponseFactory(
            response_set=self.response_set,
            eligible=True,
        )
        self.age_when_started_smoking_response = AgeWhenStartedSmokingResponseFactory(
            response_set=self.response_set,
            value=self.date_of_birth_response.age_in_years() - 20,
        )
        self.response = WhenYouQuitSmokingResponseFactory(
            response_set=self.response_set,
            value=self.age_when_started_smoking_response.value + 2
        )

    def test_is_valid_with_valid_input(self):
        age_when_quit = self.age_when_started_smoking_response.value + 1
        form = WhenYouQuitSmokingForm(instance=self.response, data={"value": age_when_quit})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["value"], age_when_quit)


    def test_has_a_required_error_message(self):
        form = WhenYouQuitSmokingForm(instance=self.response, data={"value": None})

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"], ["Enter your age when you quit smoking"]
        )


    def test_is_invalid_with_an_invalid_value(self):
        form = WhenYouQuitSmokingForm(
            instance=self.response, data={"value": "invalid"}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"], ["Enter your age when you quit smoking"]
        )


    def test_is_invalid_when_zero_is_entered(self):
        form = WhenYouQuitSmokingForm(instance=self.response, data={"value": 0})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["The age you quit smoking must be between 1 and your current age"],
        )

    def test_is_invalid_if_no_date_of_birth(self):
        response_set = ResponseSetFactory()
        response = WhenYouQuitSmokingResponse(response_set=response_set)
        form = WhenYouQuitSmokingForm(instance=response, data={"value": 70})

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            [
                '<a href="/date-of-birth">Provide your date of birth</a> before answering when you quit smoking'
            ],
        )

    def test_is_invalid_when_age_entered_greater_than_current_age(self):
        form = WhenYouQuitSmokingForm(instance=self.response, data={"value": 80})

        self.assertFalse(form.is_valid())

        self.assertEqual(
            form.errors["value"],
            [
                "The age you quit smoking must be the same as, or less than, your current age"
            ],
        )

    def test_deletes_periods_when_stopped_smoking_response_if_age_started_smoking_is_changed(
        self,
    ):
        self.response.value = self.age_when_started_smoking_response.value + 2
        self.response.save()

        PeriodsWhenYouStoppedSmokingResponseFactory.create(
            response_set=self.response_set,
            value=True,
            duration_years=self.age_when_started_smoking_response.years_smoked_including_stopped() - 1,
        )
        form = AgeWhenStartedSmokingForm(instance=self.response, data={"value": self.date_of_birth_response.age_in_years() - 20})
        form.save()

        self.assertFalse(
            PeriodsWhenYouStoppedSmokingResponse.objects.filter(
                response_set=self.response_set
            ).exists()
        )


    def test_does_not_delete_periods_when_stopped_smoking_response_if_age_started_smoking_is_not_changed(
        self,
    ):
        self.response.value = self.age_when_started_smoking_response.value + 1
        self.response.save()

        PeriodsWhenYouStoppedSmokingResponseFactory.create(
            response_set=self.response_set,
            value=True,
            duration_years=self.age_when_started_smoking_response.years_smoked_including_stopped() - 1,
        )

        form = AgeWhenStartedSmokingForm(instance=self.response, data={"value": self.age_when_started_smoking_response.value + 1})
        form.save()

        self.assertTrue(
            PeriodsWhenYouStoppedSmokingResponse.objects.filter(
                response_set=self.response_set
            ).exists()
        )
