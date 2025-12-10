from django.shortcuts import render, redirect

from .authenticated_view import AuthenticatedView
from lung_cancer_screening.questions.forms.metric_height_form import MetricHeightForm
from lung_cancer_screening.questions.forms.imperial_height_form import ImperialHeightForm

class HeightView(AuthenticatedView):
    def get(self, request):
        unit = request.GET.get('unit')
        form_klass = ImperialHeightForm if unit == "imperial" else MetricHeightForm

        return render(
            request,
            "height.jinja",
            {
                "form": form_klass(user=request.user),
                "unit": unit,
                "switch_to_unit": "metric" if unit == "imperial" else "imperial"
            }
        )


    def post(self, request):
        unit = request.GET.get('unit')
        form_klass = ImperialHeightForm if unit == "imperial" else MetricHeightForm

        if request.method == "POST":
            form = form_klass(
                instance = request.user.responseset_set.last(),
                data=request.POST,
                user=request.user
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
