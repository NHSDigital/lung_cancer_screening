from django.shortcuts import render, redirect
from django.urls import reverse

from .decorators.participant_decorators import require_participant, require_unsubmitted_response_set
from ..forms.have_you_ever_smoked_form import HaveYouEverSmokedForm
from ..models.response_set import HaveYouEverSmokedValues

@require_participant
@require_unsubmitted_response_set
def have_you_ever_smoked(request):
    if request.method == "POST":
        form = HaveYouEverSmokedForm(
            data=request.POST, participant=request.participant
        )

        if form.is_valid():
            has_smoked_values = (HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY.value, HaveYouEverSmokedValues.YES_I_CURRENTLY_SMOKE.value)
            have_you_ever_smoked = form.cleaned_data["have_you_ever_smoked"]

            if have_you_ever_smoked in has_smoked_values:
                response_set = request.participant.unsubmitted_response_sets().last()
                response_set.have_you_ever_smoked = have_you_ever_smoked
                response_set.save()

                return redirect(reverse("questions:date_of_birth"))
            else:
                return redirect(reverse("questions:non_smoker_exit"))

        else:
            return render(
                request,
                "have_you_ever_smoked.jinja",
                { "form": form },
                status=422
            )

    return render(
        request,
        "have_you_ever_smoked.jinja",
        {"form": HaveYouEverSmokedForm(participant=request.participant)}
    )
