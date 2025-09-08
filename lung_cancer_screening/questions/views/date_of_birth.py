from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import date
from dateutil.relativedelta import relativedelta

from .decorators.participant_decorators import require_participant

from ..models.date_response import DateResponse
from ..forms.date_response_form import DateResponseForm

@require_participant
def date_of_birth(request):
    if request.method == "POST":
        form = DateResponseForm(request.POST)

        if form.is_valid():
            fifty_five_years_ago = date.today() - relativedelta(years=55)
            seventy_five_years_ago = date.today() - relativedelta(years=75)

            if (seventy_five_years_ago < form.cleaned_data["value"] <= fifty_five_years_ago):
                DateResponse.objects.create(
                    participant=request.participant,
                    value=form.cleaned_data["value"],
                    question="What is your date of birth?"
                )

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
        { "form": DateResponseForm() }
    )
