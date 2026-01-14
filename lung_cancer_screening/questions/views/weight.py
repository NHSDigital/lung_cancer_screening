from django.urls import reverse_lazy

from .question_base_view import QuestionBaseView
from lung_cancer_screening.questions.forms.metric_weight_form import (
    MetricWeightForm
)
from lung_cancer_screening.questions.forms.imperial_weight_form import (
    ImperialWeightForm
)
from ..models.weight_response import WeightResponse


class WeightView(QuestionBaseView):
    template_name = "weight.jinja"
    model = WeightResponse
    success_url = reverse_lazy("questions:sex_at_birth")
    back_link_url = reverse_lazy("questions:height")

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
