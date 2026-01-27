from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .question_base_view import QuestionBaseView
from ..forms.currently_smoking_cigarettes_form import CurrentlySmokingCigarettesForm
from ..models.currently_smoking_cigarettes_response import CurrentlySmokingCigarettesResponse


class CurrentlySmokingCigarettesView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, QuestionBaseView):
    template_name = "question_form.jinja"
    form_class = CurrentlySmokingCigarettesForm
    model = CurrentlySmokingCigarettesResponse
    success_url = reverse_lazy("questions:responses")
    back_link_url = reverse_lazy("questions:age_when_started_smoking")
