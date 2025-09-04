from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ValidationError

from lung_cancer_screening.questions.models.participant import Participant

def non_smoker_exit(request):
    return render(
        request,
        "non_smoker_exit.jinja"
    )
