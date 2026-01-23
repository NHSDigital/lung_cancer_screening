from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .question_base_view import QuestionBaseView
from ..forms.family_history_lung_cancer_form import FamilyHistoryLungCancerForm
from ..models.family_history_lung_cancer_response import (
    FamilyHistoryLungCancerResponse
)


class FamilyHistoryLungCancerView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, QuestionBaseView):
    template_name = "family_history_lung_cancer.jinja"
    form_class = FamilyHistoryLungCancerForm
    model = FamilyHistoryLungCancerResponse
    success_url = reverse_lazy("questions:age_when_started_smoking")
    back_link_url = reverse_lazy("questions:cancer_diagnosis")

    def get_success_url(self):
        if self.object.is_truthy():
            if self.should_redirect_to_responses(self.request):
                return reverse(
                    "questions:relatives_age_when_diagnosed",
                    query={"change": "True"}
                )
            else:
                return reverse("questions:relatives_age_when_diagnosed")
        else:
            return super().get_success_url()
