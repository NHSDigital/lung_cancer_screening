from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from .decorators.participant_decorators import require_participant, require_unsubmitted_response_set

@require_participant
@require_unsubmitted_response_set
def responses(request):
    response_set = request.participant.unsubmitted_response_sets().last()

    if request.method == "POST":
        response_set.submitted_at = timezone.now()
        response_set.save()

        return redirect(reverse("questions:your_results"))

    return render(
        request,
        "responses.jinja",
        {"response_set": response_set}
    )
