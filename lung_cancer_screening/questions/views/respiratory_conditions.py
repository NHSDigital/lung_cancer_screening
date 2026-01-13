from django.shortcuts import render
from django.urls import reverse

from .question_base_view import QuestionBaseView
from ..forms.respiratory_conditions_form import RespiratoryConditionsForm
from ..models.respiratory_conditions_response import RespiratoryConditionsResponse


class RespiratoryConditionsView(QuestionBaseView):
    def get(self, request):
        response, _ = RespiratoryConditionsResponse.objects.get_or_build(
            response_set=request.response_set
        )
        return render_template(
            request,
            RespiratoryConditionsForm(instance=response)
        )

    def post(self, request):
        response, _ = RespiratoryConditionsResponse.objects.get_or_build(
            response_set=request.response_set
        )
        form = RespiratoryConditionsForm(
            instance=response,
            data=request.POST
        )

        if form.is_valid():
            response.value = form.cleaned_data["value"]
            response.save()
            return self.redirect_to_response_or_next_question(
                request,
                "questions:asbestos_exposure"
            )
        else:
            return render_template(
                request,
                form,
                status=422
            )


def render_template(request, form, status=200):
    return render(
        request,
        "question_form.jinja",
        {
            "form": form,
            "back_link_url": reverse("questions:education")
        },
        status=status
    )
