from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet


class RelativesAgeWhenDiagnosedView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        return render_template(request)

    def post(self, request):
        return redirect(reverse("questions:responses"))


def render_template(request, status=200):
    return render(
        request,
        "question_form.jinja",
        {
            "back_link_url": reverse("questions:family_history_lung_cancer")
        },
        status=status
    )
