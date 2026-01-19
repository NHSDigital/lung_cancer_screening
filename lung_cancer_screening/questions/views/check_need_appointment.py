from django.urls import reverse, reverse_lazy

from .question_base_view import QuestionBaseView
from ..forms.check_need_appointment_form import CheckNeedAppointmentForm
from ..models.check_need_appointment_response import (
    CheckNeedAppointmentResponse
)


class CheckNeedAppointmentView(QuestionBaseView):
    template_name = "check_need_appointment.jinja"
    form_class = CheckNeedAppointmentForm
    model = CheckNeedAppointmentResponse
    success_url = reverse_lazy("questions:height")
    back_link_url = reverse_lazy("questions:date_of_birth")

    def get_success_url(self):
        if self.object.value:
            return reverse("questions:book_an_appointment")
        else:
            return super().get_success_url()
