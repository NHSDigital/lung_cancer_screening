from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .question_base_view import QuestionBaseView
from ..forms.periods_when_you_stopped_smoking_form import PeriodsWhenYouStoppedSmokingForm
from ..models.periods_when_you_stopped_smoking_response import PeriodsWhenYouStoppedSmokingResponse


class PeriodsWhenYouStoppedSmokingView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, QuestionBaseView):
    template_name = "periods_when_you_stopped_smoking.jinja"
    form_class = PeriodsWhenYouStoppedSmokingForm
    model = PeriodsWhenYouStoppedSmokingResponse
    success_url = reverse_lazy("questions:responses")

    def get_back_link_url(self):
        response_set = self.request.response_set
        if hasattr(response_set, "family_history_lung_cancer_response") and response_set.family_history_lung_cancer_response.is_truthy():
            return reverse("questions:relatives_age_when_diagnosed")
        else:
            return reverse("questions:family_history_lung_cancer")

