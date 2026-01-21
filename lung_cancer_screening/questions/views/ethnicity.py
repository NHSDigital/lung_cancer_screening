from django.urls import reverse_lazy

from .question_base_view import QuestionBaseView
from ..forms.ethnicity_form import EthnicityForm
from ..models.ethnicity_response import EthnicityResponse


class EthnicityView(QuestionBaseView):
    template_name = "ethnicity.jinja"
    form_class = EthnicityForm
    model = EthnicityResponse
    success_url = reverse_lazy("questions:education")
    back_link_url = reverse_lazy("questions:gender")
