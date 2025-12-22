from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet
from ..forms.respiratory_conditions_form import RespiratoryConditionsForm
from ..models.respiratory_conditions_response import RespiratoryConditionsResponse


class RespiratoryConditionsView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        response, _ = RespiratoryConditionsResponse.objects.get_or_build(
            response_set=request.response_set
        )
        return render_template(
            request,
            RespiratoryConditionsForm(instance=response)
        )

    def post(self, request):
        response, _ = RespiratoryConditionsResponse.objects.get_or_build(
            response_set=request.response_set
        )
        form = RespiratoryConditionsForm(
            instance=response,
            data=request.POST
        )

        if form.is_valid():
            response.value = form.cleaned_data["value"]
            response.save()
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
