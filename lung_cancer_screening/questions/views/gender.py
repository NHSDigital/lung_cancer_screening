from django.shortcuts import render, redirect
from django.urls import reverse

from .decorators.participant_decorators import require_participant
from ..forms.gender_form import GenderForm

@require_participant
def gender(request):
    if request.method == "POST":
        form = GenderForm(
            participant=request.participant,
            data=request.POST
        )

        if form.is_valid():
                response_set = request.participant.responseset_set.last()
                response_set.gender = form.cleaned_data["gender"]
                response_set.save()
                return redirect(reverse("questions:responses"))
        else:
            return render(
                request,
                "gender.jinja",
                { "form": form },
                status=422
            )

    return render(
        request,
        "gender.jinja",
        { "form": GenderForm(participant=request.participant) }
    )
