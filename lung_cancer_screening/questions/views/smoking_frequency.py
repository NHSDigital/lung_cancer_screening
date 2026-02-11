from django.urls import reverse
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

    def get_success_url(self):
        return reverse(
            "questions:smoked_amount",
            kwargs={"tobacco_type": self.kwargs["tobacco_type"]},
            query=self.get_change_query_params(),
        )


    def get_back_link_url(self):
        return reverse(
            "questions:smoked_total_years",
            kwargs={"tobacco_type": self.kwargs["tobacco_type"]},
            query=self.get_change_query_params(),
        )
