from django.urls import reverse_lazy

from .question_base_view import QuestionBaseView
from lung_cancer_screening.questions.forms.metric_height_form import (
    MetricHeightForm
)
from lung_cancer_screening.questions.forms.imperial_height_form import (
    ImperialHeightForm
)
from ..models.height_response import HeightResponse


class HeightView(QuestionBaseView):
    template_name = "height.jinja"
    model = HeightResponse
    success_url = reverse_lazy("questions:weight")
    back_link_url = reverse_lazy("questions:check_need_appointment")

    def get_form_class(self):
        unit = self.get_unit()
        return ImperialHeightForm if unit == "imperial" else MetricHeightForm

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
