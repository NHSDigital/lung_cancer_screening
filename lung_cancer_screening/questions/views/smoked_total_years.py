from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .mixins.ensure_smoking_history_for_type import EnsureSmokingHistoryForTypeMixin
from .smoking_history_question_base_view import SmokingHistoryQuestionBaseView
from ..forms.smoked_total_years_form import SmokedTotalYearsForm
from ..models.smoked_total_years_response import SmokedTotalYearsResponse


class EnsureAnsweredAgeWhenStartedSmokingMixin:
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.response_set, 'age_when_started_smoking_response'):
            return redirect(reverse("questions:age_when_started_smoking"))
        else:
            return super().dispatch(request, *args, **kwargs)


class SmokedTotalYearsView(
    LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin,
    EnsureSmokingHistoryForTypeMixin, EnsureAnsweredAgeWhenStartedSmokingMixin,
    SmokingHistoryQuestionBaseView
):
    template_name = "question_form.jinja"
    form_class = SmokedTotalYearsForm
    model = SmokedTotalYearsResponse

    def get_success_url(self):
        return reverse(
            "questions:smoking_frequency",
            kwargs={"tobacco_type": self.kwargs["tobacco_type"]},
            query=self.get_change_query_params(),
        )

    def get_back_link_url(self):

        return reverse(
            "questions:smoking_current",
            kwargs={"tobacco_type": self.kwargs["tobacco_type"]},
            query=self.get_change_query_params(),
        )
