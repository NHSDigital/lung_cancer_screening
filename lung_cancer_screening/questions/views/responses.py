from django.shortcuts import render, redirect
from django.urls import reverse

from ..models.participant import Participant
from ..models.date_response import DateResponse

def responses(request):
    try:
        participant = Participant.objects.get(unique_id=request.session['participant_id'])
    except Participant.DoesNotExist:
        return redirect(reverse("questions:start"))

    return render(
        request,
        "responses.jinja",
        {"responses": participant.responses()}
    )
