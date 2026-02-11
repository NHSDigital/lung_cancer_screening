from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .mixins.ensure_smoking_history_for_type import EnsureSmokingHistoryForTypeMixin
from ..forms.smoking_change_form import SmokingChangeForm


class SmokingChangeView(
    LoginRequiredMixin,
    EnsureResponseSet,
    EnsureEligibleMixin,
    EnsureSmokingHistoryForTypeMixin,
    FormView,
):
    template_name = "question_form.jinja"
    form_class = SmokingChangeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["response_set"] = self.request.response_set
        kwargs["tobacco_type"] = self.kwargs["tobacco_type"]
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
        if self.request.POST.get("change"):
            return reverse("questions:responses")

        return reverse("questions:responses")
