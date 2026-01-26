from django.urls import reverse_lazy
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
    success_url = reverse_lazy("questions:responses")
    back_link_url = reverse_lazy("questions:age_when_started_smoking")
