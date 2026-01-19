from django.urls import reverse_lazy

from .question_base_view import QuestionBaseView
from ..forms.education_form import EducationForm
from ..models.education_response import EducationResponse


class EducationView(QuestionBaseView):
    template_name = "education.jinja"
    form_class = EducationForm
    model = EducationResponse
    success_url = reverse_lazy("questions:respiratory_conditions")
    back_link_url = reverse_lazy("questions:ethnicity")
