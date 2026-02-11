from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from lung_cancer_screening.questions.views.smoking_history_question_base_view import SmokingHistoryQuestionBaseView

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from ..forms.smoking_current_form import SmokingCurrentForm
from ..models.smoking_current_response import SmokingCurrentResponse


class SmokingCurrentView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, SmokingHistoryQuestionBaseView):
    template_name = "question_form.jinja"
    form_class = SmokingCurrentForm
    model = SmokingCurrentResponse
    back_link_url = reverse_lazy("questions:age_when_started_smoking")

    def get_success_url(self):
        return reverse(
            "questions:smoked_total_years",
            kwargs={"tobacco_type": self.kwargs["tobacco_type"]},
            query=self.get_change_query_params(),
        )

