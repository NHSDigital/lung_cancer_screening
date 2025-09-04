from django.shortcuts import render

from .decorators.participant_decorators import require_participant

@require_participant
def age_range_exit(request):
    return render(
        request,
        "age_range_exit.jinja"
    )
