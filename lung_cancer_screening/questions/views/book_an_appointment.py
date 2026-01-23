from django.shortcuts import render
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet


class BookAnAppointmentExitView(EnsureResponseSet, View):
    def get(self, request):
        return render(
            request,
            "book_an_appointment.jinja"
        )
