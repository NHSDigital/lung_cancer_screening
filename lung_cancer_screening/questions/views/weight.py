from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_response_set import EnsureResponseSet
from .mixins.ensure_eligible import EnsureEligibleMixin
from .question_base_view import QuestionBaseView
from lung_cancer_screening.questions.forms.metric_weight_form import (
    MetricWeightForm
)
from lung_cancer_screening.questions.forms.imperial_weight_form import (
    ImperialWeightForm
)
from ..models.weight_response import WeightResponse


class WeightView(LoginRequiredMixin, EnsureResponseSet, EnsureEligibleMixin, QuestionBaseView):
    template_name = "weight.jinja"
    model = WeightResponse
    success_url = reverse_lazy("questions:gender")

    def get_form_class(self):
        unit = self.get_unit()
        return ImperialWeightForm if unit == "imperial" else MetricWeightForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unit = self.get_unit()
        context["unit"] = unit
        context["switch_to_unit"] = (
            "metric" if unit == "imperial" else "imperial"
        )
        return context

    def get_unit(self):
        unit = self.request.GET.get('unit')
        response = self.get_object()
        if response.imperial and unit != "metric":
            unit = "imperial"
        return unit

    def get_back_link_url(self):
        if self.is_changing_responses():
            return reverse("questions:responses")
        return reverse("questions:height")
