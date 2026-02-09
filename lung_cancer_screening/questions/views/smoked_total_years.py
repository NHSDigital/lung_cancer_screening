from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
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
    success_url = reverse_lazy("questions:smoking_frequency", kwargs={
        "tobacco_type": "cigarettes"
    })
    back_link_url = reverse_lazy("questions:types_tobacco_smoking")
