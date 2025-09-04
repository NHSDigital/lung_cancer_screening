from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

from .decorators.participant_decorators import require_participant

from ..models.date_response import DateResponse

@require_participant
def date_of_birth(request):
    if request.method == "POST":
        try:
            value = date(
                int(request.POST['year']),
                int(request.POST['month']),
                int(request.POST['day'])
            )

            fifty_five_years_ago = date.today() - relativedelta(years=55)
            seventy_five_years_ago = date.today() - relativedelta(years=75)

            if (seventy_five_years_ago < value <= fifty_five_years_ago):
                DateResponse.objects.create(
                    participant=request.participant,
                    value=value,
                    question="What is your date of birth?"
                )

                return redirect(reverse("questions:responses"))
            else:
                return redirect(reverse("questions:age_range_exit"))

        except (ValueError, ValidationError):
            return render(
                request,
                "date_of_birth.jinja",
                status=422
            )

    return render(
        request,
        "date_of_birth.jinja"
    )
