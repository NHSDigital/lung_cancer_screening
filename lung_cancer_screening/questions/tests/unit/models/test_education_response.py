from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.education_response_factory import EducationResponseFactory

from ....models.education_response import EducationResponse, EducationValues

@tag("Education")
class TestEducationResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = EducationResponseFactory.build(response_set=self.response_set)
        model.full_clean()

    def test_has_response_set_as_foreign_key(self):
        response = EducationResponse.objects.create(
            response_set=self.response_set,
            value=[EducationValues.A_LEVELS]
        )

        self.assertEqual(response.response_set, self.response_set)

    def test_has_value_as_list_of_strings(self):
        response = EducationResponse.objects.create(
            response_set=self.response_set,
            value=[EducationValues.A_LEVELS]
        )

        self.assertIsInstance(response.value, list)
        self.assertIsInstance(response.value[0], str)
