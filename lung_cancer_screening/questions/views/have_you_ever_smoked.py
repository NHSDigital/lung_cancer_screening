from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ValidationError

from .decorators.participant_decorators import require_participant

from ..models.boolean_response import BooleanResponse

@require_participant
def have_you_ever_smoked(request):
    if request.method == "POST":
        try:
            value = int(request.POST['value'])

            if value:
                BooleanResponse.objects.create(
                    participant=request.participant,
                    value=value,
                    question="Have you ever smoked?"
                )

                return redirect(reverse("questions:date_of_birth"))
            else:
                return redirect(reverse("questions:non_smoker_exit"))

        except (ValueError, ValidationError):
            return render(
                request,
                "have_you_ever_smoked.jinja",
                status=422
            )

    return render(
        request,
        "have_you_ever_smoked.jinja"
    )
