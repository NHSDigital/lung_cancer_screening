from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .decorators.participant_decorators import require_participant
from ..forms.ethnicity_form import EthnicityForm

@require_http_methods(["GET", "POST"])
@require_participant
def ethnicity(request):

    if request.method == "POST":
        form = EthnicityForm(
            participant=request.participant,
            data=request.POST
        )

        if form.is_valid():
            response_set = request.participant.responseset_set.last()
            response_set.ethnicity = form.cleaned_data["ethnicity"]
            response_set.save()
            return redirect(reverse("questions:asbestos_exposure"))
        else:
            return render(
                request,
                "ethnicity.jinja",
                { "form": form },
                status=422
            )

    return render(
        request,
        "ethnicity.jinja",
        { "form": EthnicityForm(participant=request.participant) }
    )
