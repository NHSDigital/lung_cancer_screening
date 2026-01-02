from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet

from ..forms.cancer_diagnosis_form import CancerDiagnosisForm
from ..models.cancer_diagnosis_response import CancerDiagnosisResponse

class CancerDiagnosisView(LoginRequiredMixin, EnsureResponseSet, View):
#    def setup(self, request):
#        super()
#        self.response, _ = CancerDiagnosisResponse.objects.get_or_build(
#            response_set=request.response_set
#        )

    def get(self, request):
        response, _ = CancerDiagnosisResponse.objects.get_or_build(
            response_set=request.response_set
        )
        return render_template(request, CancerDiagnosisForm(instance=response))

    def post(self, request):
        response, _ = CancerDiagnosisResponse.objects.get_or_build(
            response_set=request.response_set
        )

        form = CancerDiagnosisForm(
            instance=response,
            data=request.POST
        )

        if form.is_valid():
            response.value = form.cleaned_data["value"]
            response.save()
            return redirect(reverse("questions:family_history_lung_cancer"))
        else:
            return render_template(request, form, 422)


def render_template(request, form, status=200):
    #response, _ = CancerDiagnosisResponse.objects.get_or_build(
    #    response_set=request.response_set
    #)

    return render(
        request,
        "cancer_diagnosis.jinja",
        {
            "form": form,
            "back_link_url": reverse("questions:asbestos_exposure")
        },
        status=status
    )
