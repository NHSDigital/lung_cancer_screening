from django.shortcuts import render, redirect
from django.urls import reverse

from .decorators.participant_decorators import require_participant
from ..forms.sex_at_birth_form import SexAtBirthForm

@require_participant
def sex_at_birth(request):
    if request.method == "POST":
        form = SexAtBirthForm(
            participant=request.participant,
            data=request.POST
        )

        if form.is_valid():
                response_set = request.participant.responseset_set.last()
                response_set.sex_at_birth = form.cleaned_data["sex_at_birth"]
                response_set.save()
                return redirect(reverse("questions:responses"))
        else:
            return render(
                request,
                "sex_at_birth.jinja",
                { "form": form },
                status=422
            )

    return render(
        request,
        "sex_at_birth.jinja",
        { "form": SexAtBirthForm(participant=request.participant) }
    )
