from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .mixins.ensure_smoking_history_for_type import EnsureSmokingHistoryForTypeMixin
from .smoking_history_question_base_view import SmokingHistoryQuestionBaseView
from ..forms.smoked_amount_form import SmokedAmountForm
from ..models.smoked_amount_response import SmokedAmountResponse


class EnsureSmokingFrequencyResponseMixin:
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self.get_object().tobacco_smoking_history, 'smoking_frequency_response'):
            return redirect(reverse(
                "questions:smoking_frequency",
                kwargs={"tobacco_type": self.kwargs["tobacco_type"]},
                query=self.get_change_query_params()
            ))

        return super().dispatch(request, *args, **kwargs)


class SmokedAmountView(
    LoginRequiredMixin,
    EnsureResponseSet,
    EnsureEligibleMixin,
    EnsureSmokingHistoryForTypeMixin,
    EnsureSmokingFrequencyResponseMixin,
    SmokingHistoryQuestionBaseView
):
    template_name = "smoked_amount.jinja"
    form_class = SmokedAmountForm
    model = SmokedAmountResponse
    success_url = reverse_lazy("questions:responses")

    def get_back_link_url(self):
        return reverse("questions:smoked_total_years", kwargs={"tobacco_type": self.kwargs["tobacco_type"]})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["frequency_text"] = self.get_frequency_text()
        return kwargs

    def get_frequency_text(self):
        return self.get_frequency_response().get_value_display_as_singleton_text()

    def get_frequency_response(self):
        return self.get_smoking_history_item().smoking_frequency_response
