from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .mixins.ensure_smoking_history_for_type import EnsureSmokingHistoryForTypeMixin
from .mixins.ensure_prerequisite_responses import EnsurePrerequisiteResponsesMixin
from .smoking_history_question_base_view import SmokingHistoryQuestionBaseView
from ..forms.smoked_total_years_form import SmokedTotalYearsForm
from ..models.smoked_total_years_response import SmokedTotalYearsResponse
from ..models.tobacco_smoking_history import TobaccoSmokingHistory


class EnsureAnsweredAgeWhenStartedSmokingMixin:
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.response_set, 'age_when_started_smoking_response'):
            return redirect(reverse("questions:age_when_started_smoking"))
        else:
            return super().dispatch(request, *args, **kwargs)

class SmokedTotalYearsView(
    LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin,
    EnsureSmokingHistoryForTypeMixin, EnsureAnsweredAgeWhenStartedSmokingMixin,
    EnsurePrerequisiteResponsesMixin,
    SmokingHistoryQuestionBaseView
):
    template_name = "question_form.jinja"
    form_class = SmokedTotalYearsForm
    model = SmokedTotalYearsResponse


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["tobacco_smoking_history"] = self.get_smoking_history_item()
        return kwargs


    def get_success_url(self):
        if self.get_smoking_history_item().is_normal():
            return reverse(
                "questions:smoking_frequency",
                kwargs={"tobacco_type": self.kwargs["tobacco_type"]},
                query=self.get_change_query_params(),
            )

        if (
            self.get_smoking_history_item().is_increased()
            and self.has_decreased_level()
        ):
            return reverse(
                "questions:smoking_frequency",
                kwargs={
                    "tobacco_type": self.kwargs["tobacco_type"],
                    "level": TobaccoSmokingHistory.Levels.DECREASED.value
                },
                query=self.get_change_query_params(),
            )

        return reverse("questions:responses")


    def get_back_link_url(self):
        if self.get_smoking_history_item().is_normal():
            return reverse(
                "questions:smoking_current",
                kwargs={"tobacco_type": self.kwargs["tobacco_type"]},
                query=self.get_change_query_params(),
            )

        return reverse(
            "questions:smoked_amount",
            kwargs=self.kwargs,
            query=self.get_change_query_params(),
        )


    def has_decreased_level(self):
        return self.request.response_set.tobacco_smoking_history.cigarettes().decreased().exists()

    def get_object_parent(self):
        return self.get_smoking_history_item()

    def get_prerequisite_responses_redirect_map(self):
        if self.get_smoking_history_item().is_normal():
            return {}

        return {
            "smoking_frequency_response": reverse(
                "questions:smoking_frequency",
                kwargs=self.kwargs,
                query=self.get_change_query_params(),
            ),
            "smoked_amount_response": reverse(
                "questions:smoked_amount",
                kwargs=self.kwargs,
                query=self.get_change_query_params(),
            ),
        }
