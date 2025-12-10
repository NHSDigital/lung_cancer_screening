from django.shortcuts import render, redirect
from django.urls import reverse

from .authenticated_view import AuthenticatedView
from ..forms.gender_form import GenderForm

class GenderView(AuthenticatedView):
    def get(self, request):
        return render_template(
            request,
            GenderForm(user=request.user),
        )

    def post(self, request):
        form = GenderForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():
                response_set = request.user.responseset_set.last()
                response_set.gender = form.cleaned_data["gender"]
                response_set.save()
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
