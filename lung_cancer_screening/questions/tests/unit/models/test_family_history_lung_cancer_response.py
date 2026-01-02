from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.family_history_lung_cancer_response_factory import FamilyHistoryLungCancerResponseFactory, FamilyHistoryLungCancerValues

from ....models.family_history_lung_cancer_response import FamilyHistoryLungCancerResponse

@tag("FamilyHistoryLungCancer")
class TestFamilyHistoryLungCancerResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = FamilyHistoryLungCancerResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = FamilyHistoryLungCancerResponse.objects.create(
            response_set=response_set,
            value=FamilyHistoryLungCancerValues.NO
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_value_as_string(self):
        response_set = ResponseSetFactory()
        response = FamilyHistoryLungCancerResponse.objects.create(
            response_set=response_set,
            value=FamilyHistoryLungCancerValues.NO
        )

        self.assertIsInstance(response.value, str)
