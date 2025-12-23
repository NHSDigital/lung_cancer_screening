from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet
from ..forms.gender_form import GenderForm
from ..models.gender_response import GenderResponse


class GenderView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        response, _ = GenderResponse.objects.get_or_build(
            response_set=request.response_set
        )
        return render_template(
            request,
            GenderForm(instance=response),
        )

    def post(self, request):
        response, _ = GenderResponse.objects.get_or_build(
            response_set=request.response_set
        )
        form = GenderForm(
            instance=response,
            data=request.POST
        )

        if form.is_valid():
            response.value = form.cleaned_data["value"]
            response.save()
            return redirect(reverse("questions:ethnicity"))
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
            "back_link_url": reverse("questions:sex_at_birth")
        },
        status=status
    )
