from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ValidationError

from lung_cancer_screening.questions.models.participant import Participant

def start(request):
    if request.method == "POST":
        try:
            participant = Participant.objects.create(
                unique_id=request.POST['participant_id']
            )

            request.session['participant_id'] = participant.unique_id

            return redirect(reverse("questions:date_of_birth"))
        except ValidationError as e:
            return render(
                request,
                "start.jinja",
                status=422
            )

    else:
        return render(
            request,
            "start.jinja"
        )
