from django.shortcuts import render

from .question_base_view import QuestionBaseView
from lung_cancer_screening.questions.forms.metric_weight_form import (
    MetricWeightForm
)
from lung_cancer_screening.questions.forms.imperial_weight_form import (
    ImperialWeightForm
)
from ..models.weight_response import WeightResponse


class WeightView(QuestionBaseView):
    def get(self, request):
        response, _ = WeightResponse.objects.get_or_build(
            response_set=request.response_set
        )

        unit = self.get_unit(request, response)

        form_klass = (
            ImperialWeightForm if unit == "imperial" else MetricWeightForm
        )

        return render(
            request,
            "weight.jinja",
            {
                "form": form_klass(instance=response),
                "unit": unit,
                "switch_to_unit": (
                    "metric" if unit == "imperial" else "imperial"
                )
            }
        )

    def post(self, request):
        response, _ = WeightResponse.objects.get_or_build(
            response_set=request.response_set
        )
        unit = self.get_unit(request, response)


        form_klass = (
            ImperialWeightForm if unit == "imperial" else MetricWeightForm
        )

        form = form_klass(
            instance=response,
            data=request.POST
        )

        if form.is_valid():
            form.save()
            return self.redirect_to_response_or_next_question(
                request,
                "questions:sex_at_birth"
            )
        else:
            return render(
                request,
                "weight.jinja",
                {
                    "form": form,
                    "unit": unit,
                    "switch_to_unit": (
                        "metric" if unit == "imperial" else "imperial"
                    )
                },
                status=422
            )

    def get_unit(self, request, response):
        unit = request.GET.get('unit')

        if response.imperial and unit != "metric":
            unit = "imperial"

        return unit
