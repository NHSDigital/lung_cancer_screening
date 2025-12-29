from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet
from ..forms.date_of_birth_form import DateOfBirthForm
from ..models.date_of_birth_response import DateOfBirthResponse


class DateOfBirthView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        response, _ = DateOfBirthResponse.objects.get_or_build(
            response_set=request.response_set
        )
        return render_template(
            request,
            DateOfBirthForm(instance=response)
        )

    def post(self, request):
        response, _ = DateOfBirthResponse.objects.get_or_build(
            response_set=request.response_set
        )
        form = DateOfBirthForm(
            instance=response,
            data=request.POST
        )

        if form.is_valid():
            fifty_five_years_ago = date.today() - relativedelta(years=55)
            seventy_five_years_ago = date.today() - relativedelta(years=75)
            date_of_birth = form.cleaned_data["value"]

            age_in_range = (
                seventy_five_years_ago < date_of_birth <= fifty_five_years_ago
            )
            if age_in_range:
                response.value = date_of_birth
                response.save()

                return redirect(reverse("questions:height"))
            else:
                return redirect(reverse("questions:age_range_exit"))

        else:
            return render_template(
                request,
                form,
                status=422
            )


def render_template(request, form, status=200):
    return render(
        request,
        "question_form.jinja",
        {
            "form": form,
            "back_link_url": reverse("questions:have_you_ever_smoked")
        },
        status=status
    )
