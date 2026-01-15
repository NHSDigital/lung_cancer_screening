from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class ConfirmationView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.responseset_set.submitted().exists():
            return redirect(reverse("questions:responses"))

        return render(
            request,
            "confirmation.jinja"
        )
