from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required

from .decorators.participant_decorators import require_participant

@login_required
@require_GET
@require_participant
def age_range_exit(request):
    return render(
        request,
        "age_range_exit.jinja"
    )
