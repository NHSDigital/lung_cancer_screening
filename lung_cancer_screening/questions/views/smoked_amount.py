from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .mixins.ensure_smoking_history_for_type import EnsureSmokingHistoryForTypeMixin
from .smoking_history_question_base_view import SmokingHistoryQuestionBaseView
from ..forms.smoked_amount_form import SmokedAmountForm
from ..models.smoked_amount_response import SmokedAmountResponse


class SmokedAmountView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, EnsureSmokingHistoryForTypeMixin, SmokingHistoryQuestionBaseView):
    template_name = "smoked_amount.jinja"
    form_class = SmokedAmountForm
    model = SmokedAmountResponse
    success_url = reverse_lazy("questions:responses")

    def get_back_link_url(self):
        return reverse("questions:smoked_total_years", kwargs={"tobacco_type": self.kwargs["tobacco_type"]})
