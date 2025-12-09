from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator

from .authenticated_view import AuthenticatedView
from .decorators.participant_decorators import require_participant
from ..forms.respiratory_conditions_form import RespiratoryConditionsForm


@method_decorator(require_participant, name="dispatch")
class RespiratoryConditionsView(AuthenticatedView):
    def get(self, request):
        return render_template(
            request,
            RespiratoryConditionsForm(participant=request.participant)
        )

    def post(self, request):
        form = RespiratoryConditionsForm(
            participant=request.participant,
            data=request.POST
        )

        if form.is_valid():
            response_set = request.participant.responseset_set.last()
            response_set.respiratory_conditions = form.cleaned_data["respiratory_conditions"]
            response_set.save()
            return redirect(reverse("questions:asbestos_exposure"))
        else:
            return render_template(
                request,
                form,
                status=422
            )

def render_template(request, form, status=200):
    return render(
        request,
        "question_form.jinja",
        {
            "form": form,
            "back_link_url": reverse("questions:education")
        },
        status=status
    )
