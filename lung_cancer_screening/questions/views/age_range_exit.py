from django.shortcuts import render
from django.views.decorators.http import require_GET

from .decorators.participant_decorators import require_participant

@require_GET
@require_participant
def age_range_exit(request):
    return render(
        request,
        "age_range_exit.jinja"
    )
