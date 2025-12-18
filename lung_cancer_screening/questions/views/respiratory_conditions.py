from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet
from ..forms.respiratory_conditions_form import RespiratoryConditionsForm


class RespiratoryConditionsView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        return render_template(
            request,
            RespiratoryConditionsForm(instance=request.response_set)
        )

    def post(self, request):
        form = RespiratoryConditionsForm(
            instance=request.response_set,
            data=request.POST
        )

        if form.is_valid():
            response_set = request.response_set
            response_set.respiratory_conditions = (
                form.cleaned_data["respiratory_conditions"]
            )
            response_set.save()
            return redirect(reverse("questions:asbestos_exposure"))
        else:
            return render_template(
                request,
                form,
                status=422
            )


def render_template(request, form, status=200):
    return render(
        request,
        "question_form.jinja",
        {
            "form": form,
            "back_link_url": reverse("questions:education")
        },
        status=status
    )
