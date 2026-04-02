from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class BookAnAppointmentExitView(LoginRequiredMixin, View):
    def get(self, request):
        return render(
            request,
            "book_an_appointment.jinja"
        )
