from django.urls import reverse_lazy

from .question_base_view import QuestionBaseView
from ..forms.respiratory_conditions_form import RespiratoryConditionsForm
from ..models.respiratory_conditions_response import RespiratoryConditionsResponse


class RespiratoryConditionsView(QuestionBaseView):
    template_name = "question_form.jinja"
    form_class = RespiratoryConditionsForm
    model = RespiratoryConditionsResponse
    success_url = reverse_lazy("questions:asbestos_exposure")
    back_link_url = reverse_lazy("questions:education")
