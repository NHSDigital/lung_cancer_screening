from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .question_base_view import QuestionBaseView
from ..forms.ethnicity_form import EthnicityForm
from ..models.ethnicity_response import EthnicityResponse


class EthnicityView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, QuestionBaseView):
    template_name = "ethnicity.jinja"
    form_class = EthnicityForm
    model = EthnicityResponse
    success_url = reverse_lazy("questions:education")

    def get_back_link_url(self):
        if self.is_changing_responses():
            return reverse("questions:responses")
        return reverse("questions:sex_at_birth")
