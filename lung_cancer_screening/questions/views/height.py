from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from lung_cancer_screening.questions.forms.metric_height_form import MetricHeightForm
from lung_cancer_screening.questions.forms.imperial_height_form import ImperialHeightForm
from .decorators.participant_decorators import require_participant

@require_http_methods(["GET", "POST"])
@require_participant
def height(request):
    unit = request.GET.get('unit')
    form_klass = ImperialHeightForm if unit == "imperial" else MetricHeightForm

    if request.method == "POST":
        form = form_klass(
            instance = request.participant.responseset_set.last(),
            data=request.POST,
            participant=request.participant
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
                    "switch_to_unit": "metric" if unit == "imperial" else "imperial"
                },
                status=422
            )

    return render(
        request,
        "height.jinja",
        {
            "form": form_klass(participant=request.participant),
            "unit": unit,
            "switch_to_unit": "metric" if unit == "imperial" else "imperial"
        }
    )

