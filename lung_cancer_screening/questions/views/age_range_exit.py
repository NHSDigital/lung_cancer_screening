from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ValidationError

from lung_cancer_screening.questions.models.participant import Participant

def age_range_exit(request):
    return render(
        request,
        "age_range_exit.jinja"
    )
