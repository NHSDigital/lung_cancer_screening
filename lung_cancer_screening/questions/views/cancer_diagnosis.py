from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .question_base_view import QuestionBaseView
from ..forms.cancer_diagnosis_form import CancerDiagnosisForm
from ..models.cancer_diagnosis_response import CancerDiagnosisResponse


class CancerDiagnosisView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, QuestionBaseView):
    template_name = "cancer_diagnosis.jinja"
    form_class = CancerDiagnosisForm
    model = CancerDiagnosisResponse
    success_url = reverse_lazy("questions:family_history_lung_cancer")

    def get_back_link_url(self):
        if self.is_changing_responses():
            return reverse("questions:responses")
        return reverse("questions:asbestos_exposure")
