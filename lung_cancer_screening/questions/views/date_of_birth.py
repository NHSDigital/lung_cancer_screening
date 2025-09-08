from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import date
from dateutil.relativedelta import relativedelta

from .decorators.participant_decorators import require_participant
from ..forms.date_of_birth_form import DateOfBirthForm

@require_participant
def date_of_birth(request):
    if request.method == "POST":
        form = DateOfBirthForm(request.POST)

        if form.is_valid():
            fifty_five_years_ago = date.today() - relativedelta(years=55)
            seventy_five_years_ago = date.today() - relativedelta(years=75)
            date_of_birth = form.cleaned_data["date_of_birth"]

            if (seventy_five_years_ago < date_of_birth <= fifty_five_years_ago):
                response_set = request.participant.responseset_set.last()
                response_set.date_of_birth = date_of_birth
                response_set.save()

                return redirect(reverse("questions:responses"))
            else:
                return redirect(reverse("questions:age_range_exit"))

        else:
            return render(
                request,
                "date_of_birth.jinja",
                { "form": form },
                status=422
            )

    return render(
        request,
        "date_of_birth.jinja",
        { "form": DateOfBirthForm() }
    )
