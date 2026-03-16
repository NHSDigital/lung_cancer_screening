from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.terms_of_use_response_factory import TermsOfUseResponseFactory

from ....models.terms_of_use_response import TermsOfUseResponse

@tag("TermsOfUse")
class TestTermsOfUseResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = TermsOfUseResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = TermsOfUseResponse.objects.create(
            response_set=response_set,
            value=True
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_value_as_bool(self):
        response_set = ResponseSetFactory()
        response = TermsOfUseResponse.objects.create(
            response_set=response_set,
            value=False
        )

        self.assertIsInstance(response.value, bool)


    def test_has_accepted_returns_true_when_value_is_true(self):
        response = TermsOfUseResponse.objects.create(
            response_set=self.response_set,
            value=True
        )

        self.assertTrue(response.has_accepted())


    def test_has_accepted_returns_false_when_value_is_false(self):
        response = TermsOfUseResponse.objects.create(
            response_set=self.response_set,
            value=False
        )

        self.assertFalse(response.has_accepted())
