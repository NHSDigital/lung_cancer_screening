from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet

from ..forms.relatives_age_when_diagnosed_form import RelativesAgeWhenDiagnosedForm
from ..models.relatives_age_when_diagnosed_response import RelativesAgeWhenDiagnosedResponse
from ..models.family_history_lung_cancer_response import FamilyHistoryLungCancerValues
class RelativesAgeWhenDiagnosedView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        response, _ = RelativesAgeWhenDiagnosedResponse.objects.get_or_build(
            response_set=request.response_set
        )

        if  hasattr(request.response_set, 'family_history_lung_cancer') and request.response_set.family_history_lung_cancer.value == FamilyHistoryLungCancerValues.YES:
            return render_template(request, RelativesAgeWhenDiagnosedForm(instance=response))
        else:
            return redirect(reverse("questions:family_history_lung_cancer"))

    def post(self, request):
        response, _ = RelativesAgeWhenDiagnosedResponse.objects.get_or_build(
            response_set=request.response_set
        )

        form = RelativesAgeWhenDiagnosedForm(
            instance=response,
            data=request.POST
        )

        if form.is_valid():
            response.value = form.cleaned_data["value"]
            response.save()

            return redirect(reverse("questions:responses"))

        else:
            return render_template(request, form, 422)


def render_template(request, form, status=200):
    return render(
        request,
        "relative_age_when_diagnosed.jinja",
        {
            "form": form,
            "back_link_url": reverse("questions:family_history_lung_cancer")
        },
        status=status
    )
