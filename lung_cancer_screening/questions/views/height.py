from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator

from lung_cancer_screening.questions.forms.metric_height_form import MetricHeightForm
from lung_cancer_screening.questions.forms.imperial_height_form import ImperialHeightForm
from .decorators.participant_decorators import require_participant

@method_decorator(require_participant, name="dispatch")
class HeightView(View):
    def get(self, request):
        unit = request.GET.get('unit')
        form_klass = ImperialHeightForm if unit == "imperial" else MetricHeightForm

        return render(
            request,
            "height.jinja",
            {
                "form": form_klass(participant=request.participant),
                "unit": unit,
                "switch_to_unit": "metric" if unit == "imperial" else "imperial"
            }
        )


    def post(self, request):
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
