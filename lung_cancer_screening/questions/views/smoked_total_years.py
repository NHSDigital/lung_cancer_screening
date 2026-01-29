from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .mixins.ensure_smoking_history_for_type import EnsureSmokingHistoryForTypeMixin
from .smoking_history_question_base_view import SmokingHistoryQuestionBaseView
from ..forms.smoked_total_years_form import SmokedTotalYearsForm
from ..models.smoked_total_years_response import SmokedTotalYearsResponse


class SmokedTotalYearsView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, EnsureSmokingHistoryForTypeMixin, SmokingHistoryQuestionBaseView):
    template_name = "question_form.jinja"
    form_class = SmokedTotalYearsForm
    model = SmokedTotalYearsResponse
    back_link_url = reverse_lazy("questions:types_tobacco_smoking")

    def get_success_url(self):
        if self.should_redirect_to_responses(self.request):
            return reverse("questions:responses")

        return reverse("questions:smoked_amount", kwargs={"tobacco_type": self.kwargs["tobacco_type"]})
