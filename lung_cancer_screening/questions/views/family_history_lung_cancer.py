from django.shortcuts import render, redirect
from django.urls import reverse

from .authenticated_view import AuthenticatedView
from .decorators.participant_decorators import require_participant
from django.utils.decorators import method_decorator

@method_decorator(require_participant, name="dispatch")
class FamilyHistoryLungCancerView(AuthenticatedView):
    def get(self, request):
        return render_template(request)

    def post(self, request):
        return redirect(reverse("questions:responses"))

def render_template(request, status=200):
    return render(
        request,
        "question_form.jinja",
        {
            "back_link_url": reverse("questions:cancer_diagnosis")
        },
        status=status
    )
