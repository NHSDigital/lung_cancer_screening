from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator


from .decorators.participant_decorators import require_participant
from ..forms.asbestos_exposure_form import AsbestosExposureForm

@method_decorator(require_participant, name="dispatch")
class AsbestosExposureView(View):
    def get(self, request):
        return render(
            request,
            "asbestos_exposure.jinja",
            {"form": AsbestosExposureForm(participant=request.participant)}
        )

    def post(self, request):
        form = AsbestosExposureForm(
            participant=request.participant,
            data=request.POST
        )

        if form.is_valid():
            response_set = request.participant.responseset_set.last()
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
