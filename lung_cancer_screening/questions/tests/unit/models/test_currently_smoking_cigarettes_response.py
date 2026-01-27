from django.test import TestCase, tag

from ....models.currently_smoking_cigarettes_response import CurrentlySmokingCigarettesResponse

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.currently_smoking_cigarettes_response_factory import CurrentlySmokingCigarettesResponseFactory

@tag("CurrentlySmokingCigarettes")
class TestCurrentlySmokingCigarettesResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = CurrentlySmokingCigarettesResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = CurrentlySmokingCigarettesResponse.objects.create(
            response_set=response_set,
            value=True
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_value_as_bool(self):
        response_set = ResponseSetFactory()
        response = CurrentlySmokingCigarettesResponse.objects.create(
            response_set=response_set,
            value=False
        )

        self.assertIsInstance(response.value, bool)
