from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

from ..models.participant import Participant
from ..models.date_response import DateResponse


def date_of_birth(request):
    try:
        participant = Participant.objects.get(
            unique_id=request.session['participant_id'])
    except Participant.DoesNotExist:
        return redirect(reverse("questions:start"))

    if request.method == "POST":
        try:
            value = date(
                int(request.POST['year']),
                int(request.POST['month']),
                int(request.POST['day'])
            )

            fifty_five_years_ago = date.today() - relativedelta(years=55)
            seventy_five_years_ago = date.today() - relativedelta(years=75)

            if value in (fifty_five_years_ago, seventy_five_years_ago):
                DateResponse.objects.create(
                    participant=participant,
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
                {"participant_id": participant.unique_id},
                status=422
            )

    return render(
        request,
        "date_of_birth.jinja",
        { "participant_id": participant.unique_id }
    )
