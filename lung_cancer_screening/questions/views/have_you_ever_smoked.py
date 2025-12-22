from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet
from ..forms.have_you_ever_smoked_form import HaveYouEverSmokedForm
from ..models.have_you_ever_smoked_response import HaveYouEverSmokedResponse, HaveYouEverSmokedValues

class HaveYouEverSmokedView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        response, _ = HaveYouEverSmokedResponse.objects.get_or_build(
            response_set=request.response_set
        )
        return render_template(
            request,
            HaveYouEverSmokedForm(
                instance=response
            )
        )

    def post(self, request):
        response, _ = HaveYouEverSmokedResponse.objects.get_or_build(
            response_set=request.response_set
        )
        form = HaveYouEverSmokedForm(
            data=request.POST, instance=response
        )

        if form.is_valid():
            has_smoked_values = (HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY.value, HaveYouEverSmokedValues.YES_I_CURRENTLY_SMOKE.value)
            have_you_ever_smoked = form.cleaned_data["value"]

            if have_you_ever_smoked in has_smoked_values:
                response.value = have_you_ever_smoked
                response.save()

                return redirect(reverse("questions:date_of_birth"))
            else:
                return redirect(reverse("questions:non_smoker_exit"))

        else:
            return render_template(
                request,
                form,
                status=422
            )


def render_template(request, form, status=200):
    return render(
        request,
        "have_you_ever_smoked.jinja",
        {
            "form": form,
            "back_link_url": reverse("questions:start")
        },
        status=status
    )
