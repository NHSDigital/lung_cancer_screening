from django.shortcuts import render, redirect
from django.urls import reverse

from .question_base_view import QuestionBaseView
from ..forms.family_history_lung_cancer_form import FamilyHistoryLungCancerForm
from ..models.family_history_lung_cancer_response import FamilyHistoryLungCancerResponse, FamilyHistoryLungCancerValues


class FamilyHistoryLungCancerView(QuestionBaseView):
    def get(self, request):
        response, _ = FamilyHistoryLungCancerResponse.objects.get_or_build(
            response_set=request.response_set
        )
        return render_template(request, FamilyHistoryLungCancerForm(instance=response))

    def post(self, request):
        response, _ = FamilyHistoryLungCancerResponse.objects.get_or_build(
            response_set=request.response_set
        )

        form = FamilyHistoryLungCancerForm(
            instance=response,
            data=request.POST
        )

        if form.is_valid():
            response.value = form.cleaned_data["value"]
            response.save()

            if response.value == FamilyHistoryLungCancerValues.YES:
                query = {"change": "True"} if self.should_redirect_to_responses(request) else None
                return redirect(reverse("questions:relatives_age_when_diagnosed", query=query))
            else:
                return self.redirect_to_response_or_next_question(
                    request,
                    "questions:responses"
                )
        else:
            return render_template(request, form, 422)



def render_template(request, form, status=200):
    return render(
        request,
        "family_history_lung_cancer.jinja",
        {
            "form": form,
            "back_link_url": reverse("questions:cancer_diagnosis")
        },
        status=status
    )
