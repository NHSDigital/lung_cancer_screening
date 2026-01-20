from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.family_history_lung_cancer_response_factory import (
    FamilyHistoryLungCancerResponseFactory,
)
from ...factories.relatives_age_when_diagnosed_response_factory import (
    RelativesAgeWhenDiagnosedResponseFactory
)

from ....models.family_history_lung_cancer_response import (
    FamilyHistoryLungCancerResponse,
    FamilyHistoryLungCancerValues,
)

@tag("FamilyHistoryLungCancer")
class TestFamilyHistoryLungCancerResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = FamilyHistoryLungCancerResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response = FamilyHistoryLungCancerResponse.objects.create(
            response_set=self.response_set,
            value=FamilyHistoryLungCancerValues.NO
        )

        self.assertEqual(response.response_set, self.response_set)

    def test_has_value_as_string(self):
        response = FamilyHistoryLungCancerResponse.objects.create(
            response_set=self.response_set,
            value=FamilyHistoryLungCancerValues.NO
        )

        self.assertIsInstance(response.value, str)


    def test_is_truthy_returns_true_if_value_is_yes(self):
        response = FamilyHistoryLungCancerResponseFactory(
            value=FamilyHistoryLungCancerValues.YES
        )

        self.assertTrue(response.is_truthy())


    def test_is_truthy_returns_false_if_value_is_no(self):
        response = FamilyHistoryLungCancerResponseFactory(
            value=FamilyHistoryLungCancerValues.NO
        )

        self.assertFalse(response.is_truthy())


    def test_deletes_family_age_when_diagnosed_if_response_is_no(self):
        RelativesAgeWhenDiagnosedResponseFactory.create(response_set=self.response_set)

        self.assertTrue(hasattr(self.response_set, "relatives_age_when_diagnosed"))

        FamilyHistoryLungCancerResponse.objects.create(
            response_set=self.response_set,
            value=FamilyHistoryLungCancerValues.NO
        )

        self.response_set.refresh_from_db()
        self.assertFalse(hasattr(self.response_set, "relatives_age_when_diagnosed"))


    def test_deletes_family_age_when_diagnosed_if_response_is_unknown(self):
        RelativesAgeWhenDiagnosedResponseFactory.create(response_set=self.response_set)

        self.assertTrue(hasattr(self.response_set, "relatives_age_when_diagnosed"))

        FamilyHistoryLungCancerResponse.objects.create(
            response_set=self.response_set,
            value=FamilyHistoryLungCancerValues.UNKNOWN
        )

        self.response_set.refresh_from_db()
        self.assertFalse(hasattr(self.response_set, "relatives_age_when_diagnosed"))


    def test_does_not_delete_family_age_when_diagnosed_if_response_is_yes(self):
        RelativesAgeWhenDiagnosedResponseFactory.create(response_set=self.response_set)

        self.assertTrue(hasattr(self.response_set, "relatives_age_when_diagnosed"))

        FamilyHistoryLungCancerResponse.objects.create(
            response_set=self.response_set,
            value=FamilyHistoryLungCancerValues.YES
        )

        self.response_set.refresh_from_db()
        self.assertTrue(hasattr(self.response_set, "relatives_age_when_diagnosed"))
