from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet
from ..forms.asbestos_exposure_form import AsbestosExposureForm
from ..models.asbestos_exposure_response import AsbestosExposureResponse

class AsbestosExposureView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        response, _ = AsbestosExposureResponse.objects.get_or_build(
            response_set=request.response_set
        )
        return render_template(
            request,
            AsbestosExposureForm(instance=response)
        )

    def post(self, request):
        response, _ = AsbestosExposureResponse.objects.get_or_build(
            response_set=request.response_set
        )
        form = AsbestosExposureForm(
            instance=response,
            data=request.POST
        )

        if form.is_valid():
            response.value = form.cleaned_data["value"]
            response.save()
            if self._should_redirect_to_responses(request):
                return redirect(reverse("questions:responses"))
            else:
                return redirect(reverse("questions:cancer_diagnosis"))
        else:
            return render_template(request, form, 422)


    def _should_redirect_to_responses(self, request):
        return bool(request.POST.get("change"))

def render_template(request, form, status=200):
    return render(
        request,
        "asbestos_exposure.jinja",
        {
            "form": form,
            "back_link_url": reverse("questions:respiratory_conditions")
        },
        status=status
    )
