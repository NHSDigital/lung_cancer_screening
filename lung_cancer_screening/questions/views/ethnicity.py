from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet
from ..forms.ethnicity_form import EthnicityForm


class EthnicityView(LoginRequiredMixin, EnsureResponseSet, View):
    def get(self, request):
        return render_template(
            request,
            EthnicityForm(instance=request.response_set)
        )

    def post(self, request):
        form = EthnicityForm(
            instance=request.response_set,
            data=request.POST
        )

        if form.is_valid():
            response_set = request.response_set
            response_set.ethnicity = form.cleaned_data["ethnicity"]
            response_set.save()
            return redirect(reverse("questions:education"))
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
            "back_link_url": reverse("questions:gender")
        },
        status=status
    )
