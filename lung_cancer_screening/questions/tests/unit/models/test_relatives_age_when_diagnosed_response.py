from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.relatives_age_when_diagnosed_response_factory import RelativesAgeWhenDiagnosedResponseFactory, RelativesAgeWhenDiagnosedValues

from ....models.relatives_age_when_diagnosed_response import RelativesAgeWhenDiagnosedResponse

@tag("FamilyHistoryLungCancer")
class TestRelativesAgeWhenDiagnosedResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = RelativesAgeWhenDiagnosedResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = RelativesAgeWhenDiagnosedResponse.objects.create(
            response_set=response_set,
            value=RelativesAgeWhenDiagnosedValues.NO
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_value_as_string(self):
        response_set = ResponseSetFactory()
        response = RelativesAgeWhenDiagnosedResponse.objects.create(
            response_set=response_set,
            value=RelativesAgeWhenDiagnosedValues.NO
        )

        self.assertIsInstance(response.value, str)
