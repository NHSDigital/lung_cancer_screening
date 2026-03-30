from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .question_base_view import QuestionBaseView
from ..forms.sex_at_birth_form import SexAtBirthForm
from ..models.sex_at_birth_response import SexAtBirthResponse


class SexAtBirthView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, QuestionBaseView):
    template_name = "sex_at_birth.jinja"
    form_class = SexAtBirthForm
    model = SexAtBirthResponse
    success_url = reverse_lazy("questions:ethnicity")

    def get_back_link_url(self):
        if self.is_changing_responses():
            return reverse("questions:responses")
        return reverse("questions:gender")
