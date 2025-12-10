from django.shortcuts import render, redirect
from django.urls import reverse

from .authenticated_view import AuthenticatedView
from ..forms.sex_at_birth_form import SexAtBirthForm

class SexAtBirthView(AuthenticatedView):
    def get(self, request):
        return render_template(
            request,
            SexAtBirthForm(user=request.user)
        )

    def post(self, request):
        form = SexAtBirthForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():
                response_set = request.user.responseset_set.last()
                response_set.sex_at_birth = form.cleaned_data["sex_at_birth"]
                response_set.save()
                return redirect(reverse("questions:gender"))
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
            "back_link_url": reverse("questions:weight")
        },
        status=status
    )
