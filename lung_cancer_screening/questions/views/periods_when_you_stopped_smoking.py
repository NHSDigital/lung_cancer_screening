from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .question_base_view import QuestionBaseView
from ..forms.periods_when_you_stopped_smoking_form import PeriodsWhenYouStoppedSmokingForm
from ..models.periods_when_you_stopped_smoking_response import PeriodsWhenYouStoppedSmokingResponse


class PeriodsWhenYouStoppedSmokingView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, QuestionBaseView):
    template_name = "periods_when_you_stopped_smoking.jinja"
    form_class = PeriodsWhenYouStoppedSmokingForm
    model = PeriodsWhenYouStoppedSmokingResponse
    success_url = reverse_lazy("questions:types_tobacco_smoking")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get("form") or self.get_form()
        context["page_title"] = form.page_title()
        return context

    def came_from_responses(self):
        return self.request.headers.get("Referer", "").endswith(
            reverse("questions:responses")
        )


    def get_back_link_url(self):
        if self.is_changing_responses() and self.came_from_responses():
            return reverse("questions:responses")

        if self.request.response_set.former_smoker():
            url_lookup = "questions:when_you_quit_smoking"
        else:
            url_lookup = "questions:age_when_started_smoking"

        return reverse(url_lookup, query=self.get_change_query_params())
