from django.test import TestCase, tag
from django.core.exceptions import ValidationError

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory

from ....models.tobacco_smoking_history import TobaccoSmokingHistoryTypes


@tag("TypesTobaccoSmoking")
class TestTobaccoSmokingHistory(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()


    def test_has_a_valid_factory(self):
        model = TobaccoSmokingHistoryFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response = TobaccoSmokingHistoryFactory.build(
            response_set=self.response_set
        )

        self.assertEqual(response.response_set, self.response_set)


    def test_has_type_as_a_string(self):
        response = TobaccoSmokingHistoryFactory.build(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES
        )

        self.assertIsInstance(response.type, str)


    def test_is_invalid_with_a_duplicate_response_set_and_type(self):
        TobaccoSmokingHistoryFactory(response_set=self.response_set, type=TobaccoSmokingHistoryTypes.CIGARETTES)

        with self.assertRaises(ValidationError):
            TobaccoSmokingHistoryFactory(response_set=self.response_set, type=TobaccoSmokingHistoryTypes.CIGARETTES)
