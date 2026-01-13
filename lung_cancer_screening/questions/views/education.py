from django.shortcuts import render
from django.urls import reverse

from .question_base_view import QuestionBaseView

from ..models.education_response import EducationResponse
from ..forms.education_form import EducationForm


class EducationView(QuestionBaseView):
    def get(self, request):
        response, _ = EducationResponse.objects.get_or_build(
            response_set=request.response_set
        )
        return render_template(
            request,
            EducationForm(instance=response)
        )

    def post(self, request):
        response, _ = EducationResponse.objects.get_or_build(
            response_set=request.response_set
        )
        form = EducationForm(
            instance=response,
            data=request.POST
        )

        if form.is_valid():
            response.value = form.cleaned_data["value"]
            response.save()
            return self.redirect_to_response_or_next_question(
                request,
                "questions:respiratory_conditions"
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
        "education.jinja",
        {
            "form": form,
            "back_link_url": reverse("questions:ethnicity")
        },
        status=status
    )
