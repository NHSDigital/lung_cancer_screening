from django.shortcuts import render, redirect
from django.urls import reverse

from ..models.participant import Participant
from ..models.questionnaire_response import QuestionnaireResponse

def responses(request):
    try:
        participant = Participant.objects.get(unique_id=request.session['participant_id'])
    except Participant.DoesNotExist:
        return redirect(reverse("questions:start"))


    questionnaire_responses = QuestionnaireResponse.objects.filter(
        participant=participant
    )

    return render(
        request,
        "responses.jinja",
        {"questionnaire_responses": questionnaire_responses}
    )
