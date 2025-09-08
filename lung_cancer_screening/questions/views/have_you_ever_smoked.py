from django.shortcuts import render, redirect
from django.urls import reverse

from .decorators.participant_decorators import require_participant

from ..models.boolean_response import BooleanResponse
from ..forms.boolean_response_form import BooleanResponseForm

@require_participant
def have_you_ever_smoked(request):
    if request.method == "POST":
        form = BooleanResponseForm(request.POST)

        if form.is_valid():
            if form.cleaned_data["value"]:
                BooleanResponse.objects.create(
                    participant=request.participant,
                    value=form.cleaned_data["value"],
                    question="Have you ever smoked?"
                )

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
        { "form": BooleanResponseForm() }
    )
