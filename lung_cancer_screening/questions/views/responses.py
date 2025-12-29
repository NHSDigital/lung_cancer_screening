from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet
from ..presenters.response_set_presenter import ResponseSetPresenter


class ResponsesView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        return render(
            request,
            "responses.jinja",
            { "response_set": ResponseSetPresenter(request.response_set) }
        )

    def post(self, request):
        response_set = request.response_set

        response_set.submitted_at = timezone.now()
        response_set.save()

        return redirect(reverse("questions:your_results"))
