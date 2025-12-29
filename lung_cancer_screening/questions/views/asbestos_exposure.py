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
        return render(
            request,
            "asbestos_exposure.jinja",
            {"form": AsbestosExposureForm(instance=response)}
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
            return redirect(reverse("questions:cancer_diagnosis"))
        else:
            return render(
                request,
                "asbestos_exposure.jinja",
                {"form": form},
                status=422
            )
