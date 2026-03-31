from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .question_base_view import QuestionBaseView
from ..forms.when_you_quit_smoking_form import WhenYouQuitSmokingForm
from ..models.when_you_quit_smoking_response import WhenYouQuitSmokingResponse


class WhenYouQuitSmokingView(
    LoginRequiredMixin,
    EnsureResponseSet,
    EnsureEligibleMixin,
    QuestionBaseView
):
    template_name = "question_form.jinja"
    form_class = WhenYouQuitSmokingForm
    model = WhenYouQuitSmokingResponse
    success_url = reverse_lazy("questions:periods_when_you_stopped_smoking")
    back_link_url = reverse_lazy("questions:age_when_started_smoking")
    # page_title = "How old were you when you started smoking? – NHS"

    def get_success_url(self):
        if self.is_changing_responses():
            return reverse(
                "questions:periods_when_you_stopped_smoking",
                query={"change": "True"}
            )
        else:
            return super().get_success_url()
