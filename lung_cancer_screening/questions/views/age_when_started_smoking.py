from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .question_base_view import QuestionBaseView
from ..forms.age_when_started_smoking_form import AgeWhenStartedSmokingForm
from ..models.age_when_started_smoking_response import AgeWhenStartedSmokingResponse

class AgeWhenStartedSmokingView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, QuestionBaseView):
    template_name = "question_form.jinja"
    form_class = AgeWhenStartedSmokingForm
    model = AgeWhenStartedSmokingResponse
    success_url = reverse_lazy("questions:responses")
    back_link_url = reverse_lazy("questions:relatives_age_when_diagnosed")
