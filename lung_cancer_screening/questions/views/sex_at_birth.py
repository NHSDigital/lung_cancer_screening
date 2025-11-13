from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator

from .decorators.participant_decorators import require_participant
from ..forms.sex_at_birth_form import SexAtBirthForm

@method_decorator(require_participant, name="dispatch")
class SexAtBirthView(View):
    def get(self, request):
        return render_template(
            request,
            SexAtBirthForm(participant=request.participant)
        )

    def post(self, request):
        form = SexAtBirthForm(
            participant=request.participant,
            data=request.POST
        )

        if form.is_valid():
                response_set = request.participant.responseset_set.last()
                response_set.sex_at_birth = form.cleaned_data["sex_at_birth"]
                response_set.save()
                return redirect(reverse("questions:gender"))
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
            "back_link_url": reverse("questions:weight")
        },
        status=status
    )
