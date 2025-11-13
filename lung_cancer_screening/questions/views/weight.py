from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator

from lung_cancer_screening.questions.forms.metric_weight_form import MetricWeightForm
from lung_cancer_screening.questions.forms.imperial_weight_form import ImperialWeightForm
from .decorators.participant_decorators import require_participant

@method_decorator(require_participant, name="dispatch")
class WeightView(View):
    def get(self, request):
        unit = request.GET.get('unit')
        form_klass = ImperialWeightForm if unit == "imperial" else MetricWeightForm

        return render(
            request,
            "weight.jinja",
            {
                "form": form_klass(participant=request.participant),
                "unit": unit,
                "switch_to_unit": "metric" if unit == "imperial" else "imperial"
            }
        )

    def post(self, request):
        unit = request.GET.get('unit')
        form_klass = ImperialWeightForm if unit == "imperial" else MetricWeightForm

        form = form_klass(
            instance=request.participant.responseset_set.last(),
            data=request.POST,
            participant=request.participant
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
