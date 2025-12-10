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


class HeightView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        unit = request.GET.get('unit')
        form_klass = (
            ImperialHeightForm if unit == "imperial" else MetricHeightForm
        )

        return render(
            request,
            "height.jinja",
            {
                "form": form_klass(instance=request.response_set),
                "unit": unit,
                "switch_to_unit": (
                    "metric" if unit == "imperial" else "imperial"
                )
            }
        )

    def post(self, request):
        unit = request.GET.get('unit')
        form_klass = (
            ImperialHeightForm if unit == "imperial" else MetricHeightForm
        )

        form = form_klass(
            instance=request.response_set,
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
