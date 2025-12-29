from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet
from lung_cancer_screening.questions.forms.metric_height_form import (
    MetricHeightForm
)
from lung_cancer_screening.questions.forms.imperial_height_form import (
    ImperialHeightForm
)
from ..models.height_response import HeightResponse


class HeightView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        response, _ = HeightResponse.objects.get_or_build(
            response_set=request.response_set
        )

        unit = self.get_unit(request, response)

        form_klass = ImperialHeightForm if unit == "imperial" else MetricHeightForm

        return render(
            request,
            "height.jinja",
            {
                "form": form_klass(instance=response),
                "unit": unit,
                "switch_to_unit": (
                    "metric" if unit == "imperial" else "imperial"
                )
            }
        )

    def post(self, request):

        response, _ = HeightResponse.objects.get_or_build(
            response_set=request.response_set
        )

        unit = self.get_unit(request, response)

        form_klass = ImperialHeightForm if unit == "imperial" else MetricHeightForm

        form = form_klass(
            instance=response,
            data=request.POST
        )

        if form.is_valid():
            form.save()

            return redirect("questions:weight")
        else:
            return render(
                request,
                "height.jinja",
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
