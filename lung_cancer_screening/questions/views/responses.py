from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator

from .authenticated_view import AuthenticatedView
from .decorators.participant_decorators import require_participant

@method_decorator(require_participant, name="dispatch")
class ResponsesView(AuthenticatedView):
    def get(self, request):
        return render(
            request,
            "responses.jinja",
            {"response_set": request.participant.responseset_set.last()}
        )

    def post(self, request):
        response_set = request.participant.responseset_set.last()

        response_set.submitted_at = timezone.now()
        response_set.save()

        return redirect(reverse("questions:your_results"))
