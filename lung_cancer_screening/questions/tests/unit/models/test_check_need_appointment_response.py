from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.check_need_appointment_response_factory import CheckNeedAppointmentResponseFactory

from ....models.check_need_appointment_response import CheckNeedAppointmentResponse

@tag("CheckNeedAppointment")
class TestCheckNeedAppointmentResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = CheckNeedAppointmentResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = CheckNeedAppointmentResponse.objects.create(
            response_set=response_set,
            value=True
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_value_as_bool(self):
        response_set = ResponseSetFactory()
        response = CheckNeedAppointmentResponse.objects.create(
            response_set=response_set,
            value=False
        )

        self.assertIsInstance(response.value, bool)


    def test_is_eligible_returns_true_when_value_is_false(self):
        response = CheckNeedAppointmentResponse.objects.create(
            response_set=self.response_set,
            value=False
        )

        self.assertTrue(response.is_eligible())


    def test_is_eligible_returns_false_when_value_is_true(self):
        response = CheckNeedAppointmentResponse.objects.create(
            response_set=self.response_set,
            value=True
        )

        self.assertFalse(response.is_eligible())
