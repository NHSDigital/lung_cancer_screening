from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet
from ..forms.ethnicity_form import EthnicityForm
from ..models.ethnicity_response import EthnicityResponse


class EthnicityView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        response, _ = EthnicityResponse.objects.get_or_build(
            response_set=request.response_set
        )
        return render_template(
            request,
            EthnicityForm(instance=response)
        )

    def post(self, request):
        response, _ = EthnicityResponse.objects.get_or_build(
            response_set=request.response_set
        )
        form = EthnicityForm(
            instance=response,
            data=request.POST
        )

        if form.is_valid():
            response.value = form.cleaned_data["value"]
            response.save()
            return redirect(reverse("questions:education"))
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
            "back_link_url": reverse("questions:gender")
        },
        status=status
    )
