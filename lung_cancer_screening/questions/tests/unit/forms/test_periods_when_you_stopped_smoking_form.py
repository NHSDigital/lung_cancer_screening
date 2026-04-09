from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory
from ...factories.periods_when_you_stopped_smoking_response_factory import PeriodsWhenYouStoppedSmokingResponseFactory
from ...factories.have_you_ever_smoked_response_factory import HaveYouEverSmokedResponseFactory

from ....forms.periods_when_you_stopped_smoking_form import PeriodsWhenYouStoppedSmokingForm


@tag("PeriodsWhenYouStoppedSmoking")
class TestPeriodsWhenYouStoppedSmokingForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.age_when_started_smoking_response = AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.response_set
        )
        self.response = PeriodsWhenYouStoppedSmokingResponseFactory.create(
            response_set=self.response_set,
            value=True,
            duration_years=1
        )
        self.valid_params = {
            "value": "True",
            "duration_years": 1
        }


    def test_clears_the_duration_years_if_value_is_no(self):
        form = PeriodsWhenYouStoppedSmokingForm(
            instance=self.response,
            data={
                "value": "False",
                "duration_years": 1
            }
        )
        form.is_valid()
        self.assertEqual(form.cleaned_data["duration_years"], None)

        form.save()
        self.response.refresh_from_db()
        self.assertEqual(self.response.duration_years, None)


    def test_has_a_label_for_current_smoker(self):
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            current_smoker=True,
        )

        form = PeriodsWhenYouStoppedSmokingForm(
            instance=self.response,
            data=self.valid_params
        )

        self.assertEqual(
            form.fields["value"].label,
            "Have you ever stopped smoking for periods of 1 year or longer?"
        )


    def test_has_a_label_for_former_smoker(self):
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            former_smoker=True,
        )

        form = PeriodsWhenYouStoppedSmokingForm(
            instance=self.response,
            data=self.valid_params,
        )

        self.assertEqual(
            form.fields["value"].label,
            "Before you quit smoking, did you ever stop for periods of 1 year or longer?",
        )


    def test_has_a_duration_years_label_for_current_smoker(self):
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            current_smoker=True,
        )

        form = PeriodsWhenYouStoppedSmokingForm(
            instance=self.response,
            data=self.valid_params,
        )

        self.assertEqual(
            form.fields["duration_years"].label,
            "Enter the total number of years you stopped smoking",
        )


    def test_has_a_duration_years_label_for_former_smoker(self):
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            former_smoker=True,
        )

        form = PeriodsWhenYouStoppedSmokingForm(
            instance=self.response,
            data=self.valid_params,
        )

        self.assertEqual(
            form.fields["duration_years"].label,
            "Enter the total number of years you stopped smoking",
        )


    def test_has_a_required_error_for_current_smoker(self):
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            current_smoker=True,
        )

        form = PeriodsWhenYouStoppedSmokingForm(
            instance=self.response,
            data={
                "value": None,
            },
        )
        form.is_valid()
        self.assertIn(
            "Select if you ever stopped smoking for periods of 1 year or longer",
            form.errors["value"],
        )


    def test_has_a_required_error_for_former_smoker(self):
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            former_smoker=True,
        )
        form = PeriodsWhenYouStoppedSmokingForm(
            instance=self.response,
            data={
                "value": None,
            },
        )
        form.is_valid()
        self.assertIn(
            "Select if you ever stopped or quit smoking for periods of 1 year or longer",
            form.errors["value"],
        )


    def test_has_a_duration_years_required_error_for_current_smoker(self):
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            current_smoker=True,
        )

        form = PeriodsWhenYouStoppedSmokingForm(
            instance=self.response,
            data={
                "value": "True",
                "duration_years": "",
            },
        )
        form.is_valid()
        self.assertIn(
            "Enter the total number of years you stopped smoking",
            form.errors["duration_years"],
        )


    def test_has_a_duration_years_required_error_for_former_smoker(self):
        HaveYouEverSmokedResponseFactory.create(
            response_set=self.response_set,
            former_smoker=True,
        )
        form = PeriodsWhenYouStoppedSmokingForm(
            instance=self.response,
            data={
                "value": "True",
                "duration_years": "",
            },
        )
        form.is_valid()
        self.assertIn(
            "Enter the total number of years you stopped or quit smoking",
            form.errors["duration_years"],
        )

