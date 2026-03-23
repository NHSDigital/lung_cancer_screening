from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from inflection import camelize, underscore, dasherize

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
    LoginRequiredMixin,
    EnsureResponseSet,
    EnsureEligibleMixin,
    EnsureSmokingHistoryForTypeMixin,
    EnsurePrerequisiteResponsesMixin,
    EnsureAnsweredAgeWhenStartedSmokingMixin,
    SmokingHistoryQuestionBaseView,
):
    template_name = "question_form.jinja"
    form_class = SmokedTotalYearsForm
    model = SmokedTotalYearsResponse


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["tobacco_smoking_history"] = self.tobacco_smoking_history_item()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.get_form().page_title()
        return context


    def get_success_url(self):
        if self.tobacco_smoking_history_item().is_normal():
            return reverse(
                "questions:smoking_frequency",
                kwargs={"tobacco_type": self.kwargs["tobacco_type"]},
                query=self.get_change_query_params(),
            )

        if (
            self.tobacco_smoking_history_item().is_increased()
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

        if self.next_unanswered_history():
            return reverse(
                "questions:smoking_current",
                kwargs={
                    "tobacco_type": self.next_unanswered_history(),
                },
                query=self.get_change_query_params(),
            )

        return reverse("questions:responses")


    def get_back_link_url(self):
        if self.tobacco_smoking_history_item().is_normal():
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
        return self.request.response_set.tobacco_smoking_history.filter(
            type=self.tobacco_smoking_history_item().type,
        ).decreased().exists()


    def prerequisite_responses(self):
        if self.tobacco_smoking_history_item().is_normal():
            return [
                "smoking_current_response",
            ]

        return [
            "smoking_frequency_response",
            "smoked_amount_response"
        ]

    def remaining_unanswered_histories(self):
        tobacco_type = camelize(underscore(self.kwargs["tobacco_type"]))
        histories = self.request.response_set.types_tobacco_smoking_history()
        return histories[histories.index(tobacco_type) + 1 :]


    def next_unanswered_history(self):
        if len(self.remaining_unanswered_histories()) < 1:
            return None

        return dasherize(underscore(self.remaining_unanswered_histories()[0]))
