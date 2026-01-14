from django.urls import reverse, reverse_lazy

from .question_base_view import QuestionBaseView
from ..forms.family_history_lung_cancer_form import FamilyHistoryLungCancerForm
from ..models.family_history_lung_cancer_response import (
    FamilyHistoryLungCancerResponse,
    FamilyHistoryLungCancerValues
)


class FamilyHistoryLungCancerView(QuestionBaseView):
    template_name = "family_history_lung_cancer.jinja"
    form_class = FamilyHistoryLungCancerForm
    model = FamilyHistoryLungCancerResponse
    success_url = reverse_lazy("questions:responses")
    back_link_url = reverse_lazy("questions:cancer_diagnosis")

    def get_success_url(self):
        if self.object.value == FamilyHistoryLungCancerValues.YES:
            if self.should_redirect_to_responses(self.request):
                return reverse(
                    "questions:relatives_age_when_diagnosed",
                    query={"change": "True"}
                )
            else:
                return reverse("questions:relatives_age_when_diagnosed")
        else:
            return super().get_success_url()
