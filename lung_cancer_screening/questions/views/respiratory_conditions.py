from django.shortcuts import render, redirect
from django.urls import reverse

from .authenticated_view import AuthenticatedView
from ..forms.respiratory_conditions_form import RespiratoryConditionsForm


class RespiratoryConditionsView(AuthenticatedView):
    def get(self, request):
        return render_template(
            request,
            RespiratoryConditionsForm(user=request.user)
        )

    def post(self, request):
        form = RespiratoryConditionsForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():
            response_set = request.user.responseset_set.last()
            response_set.respiratory_conditions = form.cleaned_data["respiratory_conditions"]
            response_set.save()
            return redirect(reverse("questions:asbestos_exposure"))
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
