from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .question_base_view import QuestionBaseView
from ..forms.asbestos_exposure_form import AsbestosExposureForm
from ..models.asbestos_exposure_response import AsbestosExposureResponse


class AsbestosExposureView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, QuestionBaseView):
    template_name = "asbestos_exposure.jinja"
    form_class = AsbestosExposureForm
    model = AsbestosExposureResponse
    success_url = reverse_lazy("questions:cancer_diagnosis")
    back_link_url = reverse_lazy("questions:respiratory_conditions")
