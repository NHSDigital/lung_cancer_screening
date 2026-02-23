from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .mixins.ensure_smoking_history_for_type import EnsureSmokingHistoryForTypeMixin
from .mixins.ensure_prerequisite_responses import EnsurePrerequisiteResponsesMixin
from .smoking_history_question_base_view import SmokingHistoryQuestionBaseView
from ..forms.smoked_amount_form import SmokedAmountForm
from ..models.smoked_amount_response import SmokedAmountResponse
from ..models.tobacco_smoking_history import TobaccoSmokingHistory

class SmokedAmountView(
    LoginRequiredMixin,
    EnsureResponseSet,
    EnsureEligibleMixin,
    EnsureSmokingHistoryForTypeMixin,
    EnsurePrerequisiteResponsesMixin,
    SmokingHistoryQuestionBaseView
):
    template_name = "smoked_amount.jinja"
    form_class = SmokedAmountForm
    model = SmokedAmountResponse


    def get_success_url(self):
        if self.get_smoking_history_item().is_normal():
            return reverse(
                "questions:smoking_change",
                kwargs={"tobacco_type": self.kwargs["tobacco_type"]},
                query=self.get_change_query_params(),
            )
        else:
            return reverse(
                "questions:smoked_total_years",
                kwargs=self.kwargs,
                query=self.get_change_query_params(),
            )

    def get_back_link_url(self):
        return reverse(
            "questions:smoking_frequency",
            kwargs=self.kwargs,
            query=self.get_change_query_params()
        )


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["tobacco_smoking_history"] = self.get_smoking_history_item()
        if self.get_smoking_history_item().level != TobaccoSmokingHistory.Levels.NORMAL:
            kwargs["normal_tobacco_smoking_history"] = self.get_normal_smoking_history_item()

        return kwargs


    def get_object_parent(self):
        return self.get_smoking_history_item()


    def get_prerequisite_responses_redirect_map(self):
        result = {
            "smoking_frequency_response": reverse(
                "questions:smoking_frequency",
                kwargs={"tobacco_type": self.kwargs["tobacco_type"]},
                query=self.get_change_query_params()
            )
        }

        if self.get_smoking_history_item().level == TobaccoSmokingHistory.Levels.NORMAL:
            result["smoking_current_response"] = reverse(
                "questions:smoking_current",
                kwargs={"tobacco_type": self.kwargs["tobacco_type"]},
                query=self.get_change_query_params()
            )

        return result
