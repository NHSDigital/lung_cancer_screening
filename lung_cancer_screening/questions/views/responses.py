from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from inflection import dasherize

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
            "back_link_url": get_back_link_url(request),
        },
        status=status,
    )

def get_back_link_url(request):
    if request.response_set.tobacco_smoking_history.exists():
        tobacco_type = request.response_set.tobacco_smoking_history.in_form_order().last().type
        return reverse("questions:smoking_change", kwargs={
            "tobacco_type": dasherize(tobacco_type).lower()
        })
    else:
        return reverse("questions:types_tobacco_smoking")
