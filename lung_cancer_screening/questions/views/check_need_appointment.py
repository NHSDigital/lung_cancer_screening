from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet
from ..forms.check_need_appointment_form import CheckNeedAppointmentForm
from ..models.check_need_appointment_response import CheckNeedAppointmentResponse

class CheckNeedAppointmentView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        response, _ = CheckNeedAppointmentResponse.objects.get_or_build(
            response_set=request.response_set
        )

        return render_template(request, CheckNeedAppointmentForm(instance=response))

    def post(self, request):
        response, _ = CheckNeedAppointmentResponse.objects.get_or_build(
            response_set=request.response_set
        )
        form = CheckNeedAppointmentForm(
            instance=response,
            data=request.POST
        )

        if form.is_valid():
            response.value = form.cleaned_data["value"]
            response.save()

            if form.cleaned_data["value"] :
                return redirect(reverse("questions:bmi_exit"))
            else :
                return redirect(reverse("questions:height"))
        else:
            return render_template(request, form, 422)

def render_template(request, form, status=200):
    return render(
        request,
        "check_need_appointment.jinja",
        {
            "form": form,
            "back_link_url": reverse("questions:date_of_birth")
        },
        status=status
    )
