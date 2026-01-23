from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from .question_base_view import QuestionBaseView
from ..forms.relatives_age_when_diagnosed_form import RelativesAgeWhenDiagnosedForm
from ..models.relatives_age_when_diagnosed_response import RelativesAgeWhenDiagnosedResponse
from ..models.family_history_lung_cancer_response import FamilyHistoryLungCancerValues


class RelativesAgeWhenDiagnosedView(QuestionBaseView):
    template_name = "relative_age_when_diagnosed.jinja"
    form_class = RelativesAgeWhenDiagnosedForm
    model = RelativesAgeWhenDiagnosedResponse
    success_url = reverse_lazy("questions:age_when_started_smoking")
    back_link_url = reverse_lazy("questions:family_history_lung_cancer")

    def get(self, request, *args, **kwargs):
        if not (
            hasattr(request.response_set, "family_history_lung_cancer") and
            request.response_set.family_history_lung_cancer.value ==
            FamilyHistoryLungCancerValues.YES
        ):
            return redirect(reverse("questions:family_history_lung_cancer"))
        return super().get(request, *args, **kwargs)
