from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from lung_cancer_screening.questions.models.tobacco_smoking_history import TobaccoSmokingHistory

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["response_set"] = self.request.response_set
        kwargs["tobacco_smoking_history_item"] = self.tobacco_smoking_history_item()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = self.get_back_link_url()
        return context

    def get_success_url(self):
        return reverse(
            "questions:smoked_amount",
            kwargs=self.kwargs,
            query=self.get_change_query_params(),
        )

    def get_back_link_url(self):
        if not self.kwargs.get("level") :
            return reverse(
                "questions:smoked_total_years",
                kwargs=self.kwargs,
                query=self.get_change_query_params(),
            )

        elif self.kwargs.get("level") == TobaccoSmokingHistory.Levels.INCREASED:
            return reverse(
                "questions:smoking_change",
                kwargs={"tobacco_type": self.kwargs.get("tobacco_type")},
                query=self.get_change_query_params(),
            )

        elif self.kwargs.get("level") == TobaccoSmokingHistory.Levels.DECREASED:
            if self._has_increased_level():
                self.tobacco_smoking_history_item()
                return reverse(
                "questions:smoked_amount",
                kwargs={"tobacco_type": self.kwargs.get("tobacco_type"), "level": TobaccoSmokingHistory.Levels.INCREASED},
                query=self.get_change_query_params(),
                )
            else :
                return reverse(
                    "questions:smoking_change",
                    kwargs={"tobacco_type": self.kwargs.get("tobacco_type")},
                    query=self.get_change_query_params(),
                )


    def _has_increased_level(self):
        return self.request.response_set.tobacco_smoking_history.filter(
                type=self.tobacco_smoking_history_item().type,
                level=TobaccoSmokingHistory.Levels.INCREASED
            ).exists()
