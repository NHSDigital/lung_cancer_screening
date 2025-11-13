from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.views import View

from lung_cancer_screening.questions.models.participant import Participant

class StartView(View):
    def get(self, request):
        return render(
            request,
            "start.jinja"
        )

    def post(self, request):
        try:
            participant, _ = Participant.objects.get_or_create(
                unique_id=request.POST['participant_id']
            )
            participant.responseset_set.create()

            request.session['participant_id'] = participant.unique_id

            return redirect(reverse("questions:have_you_ever_smoked"))
        except ValidationError as e:
            return render(
                request,
                "start.jinja",
                {"error_messages": [{ "text": message } for message in e.messages ]},
                status=422
            )
