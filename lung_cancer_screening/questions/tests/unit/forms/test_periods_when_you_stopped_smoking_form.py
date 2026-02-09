from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory
from ...factories.periods_when_you_stopped_smoking_response_factory import PeriodsWhenYouStoppedSmokingResponseFactory
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
