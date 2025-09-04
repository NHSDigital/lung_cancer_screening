from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ValidationError

from ..models.participant import Participant
from ..models.boolean_response import BooleanResponse


def have_you_ever_smoked(request):
    try:
        participant = Participant.objects.get(
            unique_id=request.session['participant_id'])
    except Participant.DoesNotExist:
        return redirect(reverse("questions:start"))

    if request.method == "POST":
        try:
            value = int(request.POST['value'])

            if value:
                BooleanResponse.objects.create(
                    participant=participant,
                    value=value,
                    question="Have you ever smoked?"
                )

                return redirect(reverse("questions:date_of_birth"))
            else:
                return redirect(reverse("questions:non_smoker_exit"))

        except (ValueError, ValidationError) as e:
            return render(
                request,
                "have_you_ever_smoked.jinja",
                {"participant_id": participant.unique_id},
                status=422
            )

    return render(
        request,
        "have_you_ever_smoked.jinja",
        {"participant_id": participant.unique_id}
    )
