from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet
from ..forms.asbestos_exposure_form import AsbestosExposureForm

class AsbestosExposureView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        return render(
            request,
            "asbestos_exposure.jinja",
            {"form": AsbestosExposureForm(instance=request.response_set)}
        )

    def post(self, request):

        form = AsbestosExposureForm(
            instance=request.response_set,
            data=request.POST
        )

        if form.is_valid():
            response_set = request.user.responseset_set.last()
            response_set.asbestos_exposure = form.cleaned_data["asbestos_exposure"]
            response_set.save()
            return redirect(reverse("questions:cancer_diagnosis"))
        else:
            return render(
                request,
                "asbestos_exposure.jinja",
                {"form": form},
                status=422
            )
