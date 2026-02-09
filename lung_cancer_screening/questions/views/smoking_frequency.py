from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .mixins.ensure_smoking_history_for_type import EnsureSmokingHistoryForTypeMixin
from .smoking_history_question_base_view import SmokingHistoryQuestionBaseView
from ..forms.smoking_frequency_form import SmokingFrequencyForm
from ..models.smoking_frequency_response import SmokingFrequencyResponse


class SmokingFrequencyView(
    LoginRequiredMixin,
    EnsureResponseSet,
    EnsureEligibleMixin,
    EnsureSmokingHistoryForTypeMixin,
    SmokingHistoryQuestionBaseView
):
    template_name = "question_form.jinja"
    form_class = SmokingFrequencyForm
    model = SmokingFrequencyResponse
    success_url = reverse_lazy("questions:responses")
    back_link_url = reverse_lazy("questions:smoked_total_years", kwargs={
        "tobacco_type": "cigarettes"
    })
