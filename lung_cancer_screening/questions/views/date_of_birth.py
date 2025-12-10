from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import date
from dateutil.relativedelta import relativedelta

from .authenticated_view import AuthenticatedView
from ..forms.date_of_birth_form import DateOfBirthForm

class DateOfBirthView(AuthenticatedView):
    def get(self, request):
        return render_template(
            request,
            DateOfBirthForm(user=request.user)
        )

    def post(self, request):
        form = DateOfBirthForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():
            fifty_five_years_ago = date.today() - relativedelta(years=55)
            seventy_five_years_ago = date.today() - relativedelta(years=75)
            date_of_birth = form.cleaned_data["date_of_birth"]

            if (seventy_five_years_ago < date_of_birth <= fifty_five_years_ago):
                response_set = request.user.responseset_set.last()
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
