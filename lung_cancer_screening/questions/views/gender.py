from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .question_base_view import QuestionBaseView
from ..forms.gender_form import GenderForm
from ..models.gender_response import GenderResponse


class GenderView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, QuestionBaseView):
    template_name = "gender.jinja"
    form_class = GenderForm
    model = GenderResponse
    success_url = reverse_lazy("questions:sex_at_birth")
    page_title: str = "Your gender identity – Check if you need a lung scan – NHS"

    def get_back_link_url(self):
        if self.is_changing_responses():
            return reverse("questions:responses")
        return reverse("questions:weight")
