from django.urls import reverse, reverse_lazy
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
    success_url = reverse_lazy("questions:periods_when_you_stopped_smoking")
    back_link_url = reverse_lazy("questions:relatives_age_when_diagnosed")

    def get_success_url(self):
        if self.should_redirect_to_responses(self.request):
            return reverse(
                "questions:periods_when_you_stopped_smoking",
                query={"change": "True"}
            )
        else:
            return super().get_success_url()
