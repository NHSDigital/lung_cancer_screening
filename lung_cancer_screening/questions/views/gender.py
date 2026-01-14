from django.urls import reverse_lazy

from .question_base_view import QuestionBaseView
from ..forms.gender_form import GenderForm
from ..models.gender_response import GenderResponse


class GenderView(QuestionBaseView):
    template_name = "question_form.jinja"
    form_class = GenderForm
    model = GenderResponse
    success_url = reverse_lazy("questions:ethnicity")
    back_link_url = reverse_lazy("questions:sex_at_birth")
