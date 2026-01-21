from django.urls import reverse_lazy

from .question_base_view import QuestionBaseView
from ..forms.sex_at_birth_form import SexAtBirthForm
from ..models.sex_at_birth_response import SexAtBirthResponse


class SexAtBirthView(QuestionBaseView):
    template_name = "sex_at_birth.jinja"
    form_class = SexAtBirthForm
    model = SexAtBirthResponse
    success_url = reverse_lazy("questions:gender")
    back_link_url = reverse_lazy("questions:weight")
