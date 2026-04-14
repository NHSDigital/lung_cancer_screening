from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

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
        context["back_link_url"] = self.get_back_link_url()
        return context

    def form_valid(self, form):
        if form.is_valid():
            form.save()

        return super(TypesTobaccoSmokingView, self).form_valid(form)

    def get_success_url(self):
        tobacco_smoking_history = self.request.response_set.tobacco_smoking_history.in_form_order()

        next_tobacco_smoking_history = (
            tobacco_smoking_history.in_form_order().first()
        )

        if (tobacco_smoking_history.count() == 1):
            return reverse("questions:smoking_frequency", kwargs={
                "tobacco_type": next_tobacco_smoking_history.url_type()
            })

        return reverse(
            "questions:smoking_current",
            kwargs={
                "tobacco_type": next_tobacco_smoking_history.url_type()
            },
        )

    def is_changing_responses(self):
        return self.request.GET.get("change") == "True" or self.request.POST.get("change") == "True"

    def get_back_link_url(self):
        if self.is_changing_responses():
            return reverse("questions:responses")
        return reverse("questions:periods_when_you_stopped_smoking")
