from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from ..presenters.response_set_presenter import ResponseSetPresenter


class ResponsesView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, View):
    def get(self, request):
        return render_template(request, request.response_set)

    def post(self, request):
        response_set = request.response_set
        response_set.submitted_at = timezone.now()

        try:
            response_set.save()

            return redirect(reverse("questions:confirmation"))
        except ValidationError:
            return render_template(request, response_set, status=422)


def render_template(request, response_set, status=200):
    return render(
        request,
        "responses.jinja",
        {
            "response_set": ResponseSetPresenter(request.response_set),
            "back_link_url": reverse("questions:types_tobacco_smoking")
        },
        status=status,
    )
