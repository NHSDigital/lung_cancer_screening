from django.shortcuts import render
from django.views.decorators.http import require_GET

from .decorators.participant_decorators import require_participant

@require_GET
@require_participant
def non_smoker_exit(request):
    return render(
        request,
        "non_smoker_exit.jinja"
    )
