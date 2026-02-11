from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from inflection import dasherize

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from ..forms.types_tobacco_smoking_form import TypesTobaccoSmokingForm


class TypesTobaccoSmokingView(
    LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, FormView
):
    template_name = "types_tobacco_smoking.jinja"
    form_class = TypesTobaccoSmokingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['response_set'] = self.request.response_set
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = reverse("questions:periods_when_you_stopped_smoking")
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.save()

        return super(TypesTobaccoSmokingView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            "questions:smoking_current",
            kwargs={
                "tobacco_type": dasherize(
                    self.request.response_set.tobacco_smoking_history.first().type
                ).lower()
            },
        )
