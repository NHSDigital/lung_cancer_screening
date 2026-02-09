from django.test import TestCase, tag

from lung_cancer_screening.questions.tests.factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory

from ....models.smoking_current_response import SmokingCurrentResponse

from ...factories.smoking_current_response_factory import SmokingCurrentResponseFactory

@tag("SmokingCurrent")
class TestSmokingCurrentResponse(TestCase):
    def setUp(self):
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory()

    def test_has_a_valid_factory(self):
        model = SmokingCurrentResponseFactory.build(tobacco_smoking_history=self.tobacco_smoking_history)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response = SmokingCurrentResponse.objects.create(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=True
        )

        self.assertEqual(response.tobacco_smoking_history, self.tobacco_smoking_history)

    def test_has_value_as_bool(self):
        response = SmokingCurrentResponse.objects.create(
            tobacco_smoking_history=self.tobacco_smoking_history,
            value=False
        )

        self.assertIsInstance(response.value, bool)
