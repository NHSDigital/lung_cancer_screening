from django.shortcuts import render

from .decorators.participant_decorators import require_participant

@require_participant
def responses(request):
    return render(
        request,
        "responses.jinja",
        {"response_set": request.participant.responseset_set.last()}
    )
