from django.shortcuts import render
from django.urls import reverse

from .question_base_view import QuestionBaseView
from ..forms.asbestos_exposure_form import AsbestosExposureForm
from ..models.asbestos_exposure_response import AsbestosExposureResponse

class AsbestosExposureView(QuestionBaseView):
    def get(self, request):
        response, _ = AsbestosExposureResponse.objects.get_or_build(
            response_set=request.response_set
        )
        return render_template(
            request,
            AsbestosExposureForm(instance=response)
        )

    def post(self, request):
        response, _ = AsbestosExposureResponse.objects.get_or_build(
            response_set=request.response_set
        )
        form = AsbestosExposureForm(
            instance=response,
            data=request.POST
        )

        if form.is_valid():
            response.value = form.cleaned_data["value"]
            response.save()
            return self.redirect_to_response_or_next_question(
                request,
                "questions:cancer_diagnosis"
            )
        else:
            return render_template(request, form, 422)

def render_template(request, form, status=200):
    return render(
        request,
        "asbestos_exposure.jinja",
        {
            "form": form,
            "back_link_url": reverse("questions:respiratory_conditions")
        },
        status=status
    )
