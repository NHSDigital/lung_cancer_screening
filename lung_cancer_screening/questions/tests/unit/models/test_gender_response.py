from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.gender_response_factory import GenderResponseFactory

from ....models.gender_response import GenderResponse, GenderValues


@tag("Gender")
class TestGenderResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = GenderResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = GenderResponse.objects.create(
            response_set=response_set,
            value=GenderValues.MALE
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_value_as_string(self):
        response_set = ResponseSetFactory()
        response = GenderResponse.objects.create(
            response_set=response_set,
            value=GenderValues.MALE
        )

        self.assertIsInstance(response.value, str)
