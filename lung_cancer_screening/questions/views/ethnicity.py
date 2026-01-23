from django.urls import reverse_lazy
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
    back_link_url = reverse_lazy("questions:gender")
