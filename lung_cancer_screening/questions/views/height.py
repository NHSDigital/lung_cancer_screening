from django.shortcuts import render, redirect

from lung_cancer_screening.questions.forms.metric_height_form import MetricHeightForm

from .decorators.participant_decorators import require_participant

@require_participant
def height(request):
    if request.method == "POST":
        form = MetricHeightForm(
            instance = request.participant.responseset_set.last(),
            data=request.POST,
            participant=request.participant
        )

        if form.is_valid():
            form.save()

            return redirect("questions:responses")
        else:
            return render(
                request,
                "height.jinja",
                { "form": form },
                status=422
            )

    unit = request.GET.get('unit')
    return render(
        request,
        "height.jinja",
        {
            "form": MetricHeightForm(participant=request.participant),
            "unit": unit,
            "switch_to_unit": "metric" if unit == "imperial" else "imperial"
        }
    )
