from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .mixins.ensure_response_set import EnsureResponseSet
from .question_base_view import QuestionBaseView
from ..forms.check_need_appointment_form import CheckNeedAppointmentForm
from ..models.check_need_appointment_response import (
    CheckNeedAppointmentResponse
)


class EnsureAgeEligible:
    def dispatch(self, request, *args, **kwargs):
        if (
            not hasattr(request.response_set, "date_of_birth_response")
            or not request.response_set.date_of_birth_response.is_eligible()
        ):
            return redirect(reverse("questions:date_of_birth"))
        else:
            return super().dispatch(request, *args, **kwargs)


class CheckNeedAppointmentView(LoginRequiredMixin, EnsureResponseSet, EnsureAgeEligible, QuestionBaseView):
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
