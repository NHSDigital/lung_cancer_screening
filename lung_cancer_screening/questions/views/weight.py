from django.shortcuts import render, redirect

from lung_cancer_screening.questions.forms.metric_weight_form import MetricWeightForm
from lung_cancer_screening.questions.forms.imperial_weight_form import ImperialWeightForm
from .decorators.participant_decorators import require_participant

@require_participant
def weight(request):
    unit = request.GET.get('unit')
    form_klass = ImperialWeightForm if unit == "imperial" else MetricWeightForm

    if request.method == "POST":
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
    return render(
        request,
        "weight.jinja",
        {
            "form": form_klass(participant=request.participant),
            "unit": unit,
            "switch_to_unit": "metric" if unit == "imperial" else "imperial"
        }
    )
