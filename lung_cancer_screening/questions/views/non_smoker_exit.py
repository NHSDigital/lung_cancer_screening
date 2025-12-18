from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet


class NonSmokerExitView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        return render(
            request,
            "non_smoker_exit.jinja"
        )
