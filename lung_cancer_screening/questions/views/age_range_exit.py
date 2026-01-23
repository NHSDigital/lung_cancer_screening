from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet


class AgeRangeExitView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        return render(
            request,
            "age_range_exit.jinja"
        )
