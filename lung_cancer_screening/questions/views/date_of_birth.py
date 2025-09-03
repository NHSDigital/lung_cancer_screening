from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import date

from ..models.participant import Participant
from ..models.questionnaire_response import QuestionnaireResponse


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

            QuestionnaireResponse.objects.create(
                participant=participant,
                value=value
            )

            return redirect(reverse("questions:responses"))

        # TODO: Understand how to do validation for dates - either model
        # or Form validator
        # except ValidationError as e:
        except Exception as e:
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
