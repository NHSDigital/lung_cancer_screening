from django.test import TestCase, tag

from datetime import datetime
from dateutil.relativedelta import relativedelta

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory

from ....models.age_when_started_smoking_response import AgeWhenStartedSmokingResponse

@tag("AgeWhenStartedSmoking")
class TestAgeWhenStartedSmokingResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = AgeWhenStartedSmokingResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = AgeWhenStartedSmokingResponse.objects.create(
            response_set=response_set,
            value=17
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_value_as_int(self):
        response_set = ResponseSetFactory()
        response = AgeWhenStartedSmokingResponse.objects.create(
            response_set=response_set,
            value=17
        )

        self.assertIsInstance(response.value, int)

