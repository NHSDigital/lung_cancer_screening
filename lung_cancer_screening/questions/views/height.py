from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from lung_cancer_screening.questions.forms.height_form import HeightForm
from lung_cancer_screening.questions.models import participant

from .decorators.participant_decorators import require_participant

@require_participant
def height(request): 
  if request.method == "POST":
    form = HeightForm(
      instance = request.participant.responseset_set.last(),
      data=request.POST, 
      participant=request.participant
    )

    if form.is_valid() :
      form.save()

      return redirect("questions:responses")
    else :
      return render(
        request,
        "height.jinja",
        { "form" : form },
        status=422
      )

  return render(
        request,
        "height.jinja",
        { "form" : HeightForm(participant=request.participant) }
    )
