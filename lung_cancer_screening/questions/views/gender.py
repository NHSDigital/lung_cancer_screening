from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .decorators.participant_decorators import require_participant
from ..forms.gender_form import GenderForm

@require_http_methods(["GET", "POST"])
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
                return redirect(reverse("questions:ethnicity"))
        else:
            return render_template(
                request,
                form,
                status=422
            )

    return render_template(
        request,
        GenderForm(participant=request.participant),
    )

def render_template(request, form, status=200):
    return render(
        request,
        "question_form.jinja",
        {
            "form": form,
            "back_link_url": reverse("questions:sex_at_birth")
        },
        status=status
    )
