from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.respiratory_conditions_response_factory import RespiratoryConditionsResponseFactory

from ....models.respiratory_conditions_response import RespiratoryConditionsResponse, RespiratoryConditionValues


class TestRespiratoryConditionsResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = RespiratoryConditionsResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = RespiratoryConditionsResponse.objects.create(
            response_set=response_set,
            value=[RespiratoryConditionValues.PNEUMONIA]
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_value_as_list(self):
        response_set = ResponseSetFactory()
        response = RespiratoryConditionsResponse.objects.create(
            response_set=response_set,
            value=[RespiratoryConditionValues.PNEUMONIA, RespiratoryConditionValues.BRONCHITIS]
        )

        self.assertIsInstance(response.value, list)
