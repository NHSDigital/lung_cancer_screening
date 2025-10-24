from django.shortcuts import render, redirect

from lung_cancer_screening.questions.forms.metric_weight_form import MetricWeightForm
from .decorators.participant_decorators import require_participant

@require_participant
def weight(request):
    unit = request.GET.get('unit')
    if request.method == "POST":
        form=MetricWeightForm(
            instance=request.participant.responseset_set.last(),
            data=request.POST,
            participant=request.participant
        )
        if form.is_valid():
            form.save()
            return redirect("questions:responses")
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
    return render(
        request,
        "weight.jinja",
        {
            "form": MetricWeightForm(participant=request.participant),
            "unit": unit,
            "switch_to_unit": "metric" if unit == "imperial" else "imperial"
        }
    )
