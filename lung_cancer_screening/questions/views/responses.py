from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from .authenticated_view import AuthenticatedView

class ResponsesView(AuthenticatedView):
    def get(self, request):
        return render(
            request,
            "responses.jinja",
            {"response_set": request.user.responseset_set.last()}
        )

    def post(self, request):
        response_set = request.user.responseset_set.last()

        response_set.submitted_at = timezone.now()
        response_set.save()

        return redirect(reverse("questions:your_results"))
