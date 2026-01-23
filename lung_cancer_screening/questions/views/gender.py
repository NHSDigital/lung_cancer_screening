from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .question_base_view import QuestionBaseView
from ..forms.gender_form import GenderForm
from ..models.gender_response import GenderResponse


class GenderView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, QuestionBaseView):
    template_name = "question_form.jinja"
    form_class = GenderForm
    model = GenderResponse
    success_url = reverse_lazy("questions:ethnicity")
    back_link_url = reverse_lazy("questions:sex_at_birth")
