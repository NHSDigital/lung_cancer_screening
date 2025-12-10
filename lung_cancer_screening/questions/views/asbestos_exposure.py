from django.shortcuts import render, redirect
from django.urls import reverse

from .authenticated_view import AuthenticatedView
from ..forms.asbestos_exposure_form import AsbestosExposureForm

class AsbestosExposureView(AuthenticatedView):
    def get(self, request):
        return render(
            request,
            "asbestos_exposure.jinja",
            {"form": AsbestosExposureForm(user=request.user)}
        )

    def post(self, request):

        form = AsbestosExposureForm(
            user=request.user,
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
