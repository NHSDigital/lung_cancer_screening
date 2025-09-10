from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

from lung_cancer_screening.questions.models.participant import Participant

def require_participant(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        try:
            request.participant = Participant.objects.get(
                unique_id=request.session['participant_id'])
        except Participant.DoesNotExist:
            return redirect(reverse("questions:start"))

        return function(request, *args, **kwargs)
    return wrap

def require_unsubmitted_response_set(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.participant.has_unsubmitted_response_set():
            return redirect(reverse("questions:start"))

        return function(request, *args, **kwargs)
    return wrap
