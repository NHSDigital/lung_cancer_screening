from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .decorators.participant_decorators import require_participant
from ..forms.asbestos_exposure_form import AsbestosExposureForm


@require_http_methods(["GET", "POST"])
@require_participant
def asbestos_exposure(request):
    if request.method == "POST":
        form = AsbestosExposureForm(
            participant=request.participant,
            data=request.POST
        )

        if form.is_valid():
            response_set = request.participant.responseset_set.last()
            response_set.asbestos_exposure = form.cleaned_data["asbestos_exposure"]
            response_set.save()
            return redirect(reverse("questions:responses"))
        else:
            return render(
                request,
                "asbestos_exposure.jinja",
                {"form": form},
                status=422
            )

    return render(
        request,
        "asbestos_exposure.jinja",
        {"form": AsbestosExposureForm(participant=request.participant)}
    )
