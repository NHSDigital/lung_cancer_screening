from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from lung_cancer_screening.questions.views.smoking_history_question_base_view import SmokingHistoryQuestionBaseView

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .mixins.ensure_smoking_history_for_type import EnsureSmokingHistoryForTypeMixin
from ..forms.smoking_current_form import SmokingCurrentForm
from ..models.smoking_current_response import SmokingCurrentResponse


class SmokingCurrentView(
    LoginRequiredMixin,
    EnsureResponseSet,
    EnsureEligibleMixin,
    EnsureSmokingHistoryForTypeMixin,
    SmokingHistoryQuestionBaseView,
):
    template_name = "question_form.jinja"
    form_class = SmokingCurrentForm
    model = SmokingCurrentResponse

    def get_success_url(self):
        return reverse(
            "questions:smoked_total_years",
            kwargs={"tobacco_type": self.kwargs["tobacco_type"]},
            query=self.get_change_query_params(),
        )


    def get_back_link_url(self):
        if self.previous_smoking_history():
            if self.previous_smoking_history().is_normal():
                return reverse(
                    "questions:smoking_change",
                    kwargs={"tobacco_type": self.previous_smoking_history().url_type()},
                    query=self.get_change_query_params(),
                )

            return reverse(
                "questions:smoked_total_years",
                kwargs={
                    "tobacco_type": self.previous_smoking_history().url_type(),
                    "level": self.previous_smoking_history().level,
                },
                query=self.get_change_query_params(),
            )

        return reverse("questions:types_tobacco_smoking")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        human_type = self.tobacco_smoking_history_item().human_type().lower()
        context["human_type"] = human_type
        context["page_title"] = f"Do you currently smoke {human_type}? – NHS"
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["tobacco_smoking_history"] = self.tobacco_smoking_history_item()
        return kwargs
