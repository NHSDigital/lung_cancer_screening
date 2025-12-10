from django.shortcuts import render, redirect

from .authenticated_view import AuthenticatedView
from lung_cancer_screening.questions.forms.metric_weight_form import MetricWeightForm
from lung_cancer_screening.questions.forms.imperial_weight_form import ImperialWeightForm

class WeightView(AuthenticatedView):
    def get(self, request):
        unit = request.GET.get('unit')
        form_klass = ImperialWeightForm if unit == "imperial" else MetricWeightForm

        return render(
            request,
            "weight.jinja",
            {
                "form": form_klass(user=request.user),
                "unit": unit,
                "switch_to_unit": "metric" if unit == "imperial" else "imperial"
            }
        )

    def post(self, request):
        unit = request.GET.get('unit')
        form_klass = ImperialWeightForm if unit == "imperial" else MetricWeightForm

        form = form_klass(
            instance=request.user.responseset_set.last(),
            data=request.POST,
            user=request.user
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
                    "switch_to_unit": "metric" if unit == "imperial" else "imperial"
                },
                status=422
            )
