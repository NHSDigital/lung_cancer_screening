from django.shortcuts import render

from .decorators.participant_decorators import require_participant, require_unsubmitted_response_set

@require_participant
@require_unsubmitted_response_set
def non_smoker_exit(request):
    return render(
        request,
        "non_smoker_exit.jinja"
    )
