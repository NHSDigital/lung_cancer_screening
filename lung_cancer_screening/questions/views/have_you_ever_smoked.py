from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet
from ..forms.have_you_ever_smoked_form import HaveYouEverSmokedForm
from ..models.response_set import HaveYouEverSmokedValues

class HaveYouEverSmokedView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        return render_template(
            request,
            HaveYouEverSmokedForm(
                instance=request.response_set
            )
        )

    def post(self, request):
        form = HaveYouEverSmokedForm(
            data=request.POST, instance=request.response_set
        )

        if form.is_valid():
            has_smoked_values = (HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY.value, HaveYouEverSmokedValues.YES_I_CURRENTLY_SMOKE.value)
            have_you_ever_smoked = form.cleaned_data["have_you_ever_smoked"]

            if have_you_ever_smoked in has_smoked_values:
                response_set = request.user.responseset_set.last()
                response_set.have_you_ever_smoked = have_you_ever_smoked
                response_set.save()

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
