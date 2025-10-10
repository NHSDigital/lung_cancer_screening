from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
#from django.urls import reverse

from .decorators.participant_decorators import require_participant

@require_participant
def height(request): 
  if request.method == "POST":
    response_set = request.participant.responseset_set.last()
    
    height = request.POST.get("height")

    if height.isdigit() and int(height) > 0 :
      height = int(height)*10
    response_set.height = height
    #response_set.height_type = request.POST.get("height_type")
    try:
      response_set.save()
      return redirect("questions:responses")
    except ValidationError:
      return render(
        request,
        "height.jinja",
        status=422
      )

  return render(
        request,
        "height.jinja",
        {}
    )