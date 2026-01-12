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
