from django.shortcuts import render

from .decorators.participant_decorators import require_participant

@require_participant
def non_smoker_exit(request):
    return render(
        request,
        "non_smoker_exit.jinja"
    )
