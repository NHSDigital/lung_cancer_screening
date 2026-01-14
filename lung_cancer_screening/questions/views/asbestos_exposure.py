from django.urls import reverse_lazy

from .question_base_view import QuestionBaseView
from ..forms.asbestos_exposure_form import AsbestosExposureForm
from ..models.asbestos_exposure_response import AsbestosExposureResponse

class AsbestosExposureView(QuestionBaseView):
    template_name = "asbestos_exposure.jinja"
    form_class = AsbestosExposureForm
    model = AsbestosExposureResponse
    success_url = reverse_lazy("questions:cancer_diagnosis")
    back_link_url = reverse_lazy("questions:respiratory_conditions")
