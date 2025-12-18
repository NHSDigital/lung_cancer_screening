from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet
from lung_cancer_screening.questions.forms.metric_weight_form import (
    MetricWeightForm
)
from lung_cancer_screening.questions.forms.imperial_weight_form import (
    ImperialWeightForm
)


class WeightView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        unit = self.get_unit(request)

        form_klass = (
            ImperialWeightForm if unit == "imperial" else MetricWeightForm
        )

        return render(
            request,
            "weight.jinja",
            {
                "form": form_klass(instance=request.response_set),
                "unit": unit,
                "switch_to_unit": (
                    "metric" if unit == "imperial" else "imperial"
                )
            }
        )

    def post(self, request):
        unit = self.get_unit(request)

        form_klass = (
            ImperialWeightForm if unit == "imperial" else MetricWeightForm
        )

        form = form_klass(
            instance=request.response_set,
            data=request.POST
        )

        if form.is_valid():
            form.save()
            return redirect("questions:sex_at_birth")
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

    def get_unit(self, request):
        unit = request.GET.get('unit')

        weight_imperial=request.response_set.weight_imperial
        if weight_imperial and unit != "metric":
            unit = "imperial"

        return unit
