from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ....models.check_need_appointment_response import CheckNeedAppointmentResponse
from ....forms.check_need_appointment_form import CheckNeedAppointmentForm

@tag("CheckNeedAppointment")
class TestCheckNeedAppointmentForm(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()
        self.response = CheckNeedAppointmentResponse.objects.create(
            response_set=self.response_set,
            value=False
        )


    def test_is_valid_with_a_valid_value(self):
        form = CheckNeedAppointmentForm(
            instance=self.response,
            data={
                "value": False
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["value"],
            False
        )

    def test_is_invalid_with_an_invalid_value(self):
        form = CheckNeedAppointmentForm(
            instance=self.response,
            data={
                "value": "invalid"
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select a valid choice. invalid is not one of the available choices."]
        )

    def test_is_invalid_when_no_option_is_selected(self):
        form = CheckNeedAppointmentForm(
            instance=self.response,
            data={
                "value": None
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["value"],
            ["Select if you can continue online"]
        )
