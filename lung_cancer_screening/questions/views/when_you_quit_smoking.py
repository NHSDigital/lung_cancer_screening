from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .mixins.ensure_prerequisite_responses import EnsurePrerequisiteResponsesMixin
from .question_base_view import QuestionBaseView
from ..forms.when_you_quit_smoking_form import WhenYouQuitSmokingForm
from ..models.when_you_quit_smoking_response import WhenYouQuitSmokingResponse


class EnsureFormerSmokerMixin():
    def get(self, request, *args, **kwargs):
        if not request.response_set.former_smoker():
            return redirect(reverse("questions:periods_when_you_stopped_smoking"))

        return super().get(request, *args, **kwargs)


class WhenYouQuitSmokingView(
    LoginRequiredMixin,
    EnsureResponseSet,
    EnsureEligibleMixin,
    EnsurePrerequisiteResponsesMixin,
    EnsureFormerSmokerMixin,
    QuestionBaseView
):
    template_name = "when_you_quit_smoking.jinja"
    form_class = WhenYouQuitSmokingForm
    model = WhenYouQuitSmokingResponse
    back_link_url = reverse_lazy("questions:age_when_started_smoking")
    prerequisite_responses = ["age_when_started_smoking_response"]

    def get_success_url(self):
        return reverse(
            "questions:periods_when_you_stopped_smoking",
            query=self.get_change_query_params()
        )
