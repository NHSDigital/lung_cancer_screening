from django.shortcuts import render
from django.urls import reverse

from .question_base_view import QuestionBaseView
from ..forms.cancer_diagnosis_form import CancerDiagnosisForm
from ..models.cancer_diagnosis_response import CancerDiagnosisResponse

class CancerDiagnosisView(QuestionBaseView):

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
            return self.redirect_to_response_or_next_question(
                request,
                "questions:family_history_lung_cancer"
            )
        else:
            return render_template(request, form, 422)


def render_template(request, form, status=200):
    return render(
        request,
        "cancer_diagnosis.jinja",
        {
            "form": form,
            "back_link_url": reverse("questions:asbestos_exposure")
        },
        status=status
    )
