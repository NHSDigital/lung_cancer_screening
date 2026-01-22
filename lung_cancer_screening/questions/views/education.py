from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .question_base_view import QuestionBaseView
from ..forms.education_form import EducationForm
from ..models.education_response import EducationResponse


class EducationView(LoginRequiredMixin, EnsureResponseSet, QuestionBaseView):
    template_name = "education.jinja"
    form_class = EducationForm
    model = EducationResponse
    success_url = reverse_lazy("questions:respiratory_conditions")
    back_link_url = reverse_lazy("questions:ethnicity")
