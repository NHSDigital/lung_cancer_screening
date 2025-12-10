from django.shortcuts import render, redirect
from django.urls import reverse

from .authenticated_view import AuthenticatedView
from ..forms.ethnicity_form import EthnicityForm

class EthnicityView(AuthenticatedView):
    def get(self, request):
        return render_template(
            request,
            EthnicityForm(user=request.user)
        )

    def post(self, request):
        form = EthnicityForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():
            response_set = request.user.responseset_set.last()
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
