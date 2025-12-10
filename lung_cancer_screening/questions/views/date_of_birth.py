from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet
from ..forms.date_of_birth_form import DateOfBirthForm


class DateOfBirthView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        return render_template(
            request,
            DateOfBirthForm(instance=request.response_set)
        )

    def post(self, request):
        form = DateOfBirthForm(
            instance=request.response_set,
            data=request.POST
        )

        if form.is_valid():
            fifty_five_years_ago = date.today() - relativedelta(years=55)
            seventy_five_years_ago = date.today() - relativedelta(years=75)
            date_of_birth = form.cleaned_data["date_of_birth"]

            age_in_range = (
                seventy_five_years_ago < date_of_birth <= fifty_five_years_ago
            )
            if age_in_range:
                response_set = request.response_set
                response_set.date_of_birth = date_of_birth
                response_set.save()

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
