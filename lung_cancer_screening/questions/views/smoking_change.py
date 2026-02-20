from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from lung_cancer_screening.questions.models.tobacco_smoking_history import TobaccoSmokingHistory

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .mixins.ensure_smoking_history_for_type import EnsureSmokingHistoryForTypeMixin
from ..forms.smoking_change_form import SmokingChangeForm

class EnsureSmokingFrequencyAndAmountResponseMixin:
    def dispatch(self, request, *args, **kwargs):
        if (
            hasattr(request.tobacco_smoking_history_item, 'smoking_frequency_response')
            and hasattr(request.tobacco_smoking_history_item, 'smoked_amount_response')
        ):
            return super().dispatch(request, *args, **kwargs)

        return redirect(reverse(
            "questions:smoked_amount",
            kwargs={"tobacco_type": kwargs["tobacco_type"]},
        ))

class SmokingChangeView(
    LoginRequiredMixin,
    EnsureResponseSet,
    EnsureEligibleMixin,
    EnsureSmokingHistoryForTypeMixin,
    EnsureSmokingFrequencyAndAmountResponseMixin,
    FormView,
):
    template_name = "question_form.jinja"
    form_class = SmokingChangeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["response_set"] = self.request.response_set
        kwargs["tobacco_smoking_history_item"] = self.request.tobacco_smoking_history_item
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = self.get_back_link_url()
        return context

    def get_back_link_url(self):
        return reverse(
            "questions:smoked_amount",
            kwargs={"tobacco_type": self.kwargs["tobacco_type"]},
        )

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


    def get_success_url(self):
        tobacco_smoking_history = self.request.response_set.tobacco_smoking_history
        if tobacco_smoking_history.filter(level=TobaccoSmokingHistory.Levels.INCREASED).exists():
            return reverse(
                "questions:smoking_frequency",
                kwargs={
                    "tobacco_type": self.kwargs["tobacco_type"],
                    "level": TobaccoSmokingHistory.Levels.INCREASED,
                },
                query=self.get_change_query_params()
            )
        elif tobacco_smoking_history.filter(level=TobaccoSmokingHistory.Levels.DECREASED).exists():
            return reverse(
                "questions:smoking_frequency",
                kwargs={
                    "tobacco_type": self.kwargs["tobacco_type"],
                    "level": TobaccoSmokingHistory.Levels.DECREASED,
                },
                query=self.get_change_query_params(),
            )
        else:
            return reverse("questions:responses")


    def should_redirect_to_responses(self, request):
        return bool(request.POST.get("change"))


    def get_change_query_params(self):
        if not self.should_redirect_to_responses(self.request):
            return {}

        return {"change": "True"}
