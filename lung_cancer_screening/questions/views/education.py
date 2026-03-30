from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .question_base_view import QuestionBaseView
from ..forms.education_form import EducationForm
from ..models.education_response import EducationResponse


class EducationView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, QuestionBaseView):
    template_name = "education.jinja"
    form_class = EducationForm
    model = EducationResponse
    success_url = reverse_lazy("questions:respiratory_conditions")

    def get_back_link_url(self):
        if self.is_changing_responses():
            return reverse("questions:responses")
        return reverse("questions:ethnicity")
