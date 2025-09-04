from django.shortcuts import render

from .decorators.participant_decorators import require_participant

@require_participant
def responses(request):
    return render(
        request,
        "responses.jinja",
        {"responses": request.participant.responses()}
    )
